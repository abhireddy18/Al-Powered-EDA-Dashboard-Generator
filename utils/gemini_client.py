"""Gemini client for analysis planning and optional artifact generation."""

from __future__ import annotations

import base64
import json
import logging
import time
from typing import Any

from google import genai
from google.genai import types

from utils.prompts import (
    ANALYSIS_PLAN_SYSTEM,
    DASHBOARD_IMAGE_PROMPT_SYSTEM,
    EDA_CODE_SYSTEM,
    build_analysis_plan_user_message,
    build_dashboard_image_user_message,
    build_eda_code_user_message,
)

logger = logging.getLogger(__name__)
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
_MAX_PROFILE_CHARS = 16_000


class GeminiClient:
    """Stateless wrapper around Gemini text and image generation."""

    def __init__(
        self,
        api_key: str,
        text_model: str,
        image_model: str,
        max_retries: int = 3,
    ):
        self._client = genai.Client(api_key=api_key)
        self._text_model = text_model
        self._image_model = image_model
        self._max_retries = max_retries
        logger.info(
            "GeminiClient initialised (text=%s, image=%s, retries=%d)",
            text_model,
            image_model,
            max_retries,
        )

    def _call_with_retry(self, fn):
        last_exc = None
        for attempt in range(1, self._max_retries + 1):
            try:
                return fn()
            except Exception as exc:
                last_exc = exc
                status = getattr(exc, "status_code", None)
                if status is None:
                    status = getattr(exc, "code", None)
                if status in _RETRYABLE_STATUS_CODES and attempt < self._max_retries:
                    wait = 2 ** (attempt - 1)
                    logger.warning(
                        "Retryable Gemini error (status=%s, attempt %d/%d), waiting %ds: %s",
                        status,
                        attempt,
                        self._max_retries,
                        wait,
                        exc,
                    )
                    time.sleep(wait)
                else:
                    raise
        raise last_exc  # type: ignore[misc]

    @staticmethod
    def _trim_profile(profile: dict[str, Any]) -> dict[str, Any]:
        import copy

        trimmed = copy.deepcopy(profile)
        if len(json.dumps(trimmed, default=str)) <= _MAX_PROFILE_CHARS:
            return trimmed
        if "sample_rows" in trimmed:
            trimmed["sample_rows"] = trimmed["sample_rows"][:3]
        if "categorical_top_values" in trimmed:
            for column, values in trimmed["categorical_top_values"].items():
                trimmed["categorical_top_values"][column] = dict(list(values.items())[:5])
        if len(json.dumps(trimmed, default=str)) > _MAX_PROFILE_CHARS:
            trimmed.pop("top_correlations", None)
            trimmed.pop("outlier_pct", None)
        if len(json.dumps(trimmed, default=str)) > _MAX_PROFILE_CHARS:
            trimmed["sample_rows"] = []
        return trimmed

    def get_analysis_plan(
        self,
        profile: dict[str, Any],
        user_request: str,
    ) -> dict[str, Any]:
        user_message = build_analysis_plan_user_message(
            self._trim_profile(profile), user_request
        )
        response = self._call_with_retry(
            lambda: self._client.models.generate_content(
                model=self._text_model,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=ANALYSIS_PLAN_SYSTEM,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
        )
        raw = response.text or ""
        logger.debug("Raw analysis-plan response:\n%s", raw)
        return json.loads(raw)

    def generate_eda_code(
        self,
        plan: dict[str, Any],
        profile: dict[str, Any],
        filename: str,
    ) -> str:
        user_message = build_eda_code_user_message(plan, profile, filename)
        response = self._call_with_retry(
            lambda: self._client.models.generate_content(
                model=self._text_model,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=EDA_CODE_SYSTEM,
                    temperature=0.2,
                ),
            )
        )
        code = _strip_code_fences(response.text or "")
        logger.debug("Generated EDA code (%d chars)", len(code))
        return code

    def generate_dashboard_image(
        self,
        kpi_results: list[dict[str, Any]],
        insights: list[str],
    ) -> bytes:
        user_message = build_dashboard_image_user_message(kpi_results, insights)
        response = self._call_with_retry(
            lambda: self._client.models.generate_content(
                model=self._image_model,
                contents=f"{DASHBOARD_IMAGE_PROMPT_SYSTEM}\n\n{user_message}",
                config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
            )
        )
        for candidate in response.candidates or []:
            if not candidate.content:
                continue
            for part in candidate.content.parts or []:
                if part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image_bytes = (
                        base64.b64decode(image_data)
                        if isinstance(image_data, str)
                        else bytes(image_data)
                    )
                    logger.info("Dashboard image generated (%d bytes)", len(image_bytes))
                    return image_bytes
        raise RuntimeError(
            "Gemini returned no image. Check that image generation is available "
            "for your API key and model."
        )


def _strip_code_fences(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines)