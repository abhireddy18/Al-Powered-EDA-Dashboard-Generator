"""
config.py – Centralised configuration for the EDA Streamlit app.

Resolution order for every setting:
  1.  st.secrets  (Streamlit Community Cloud / local secrets.toml)
  2.  os.environ  (populated from .env via python-dotenv at import time)
  3.  Hard-coded default (only for model names – never for the API key)
"""

from __future__ import annotations

import os
from dotenv import load_dotenv

# Load .env file for local development (no-op in Streamlit Cloud)
load_dotenv()


def _get_secret(key: str, default: str | None = None) -> str | None:
    """
    Return a config value by checking st.secrets first, then os.environ,
    then the provided default.  Works identically on Streamlit Cloud and
    locally without code changes.
    """
    # 1. Try Streamlit secrets (gracefully handle import / key errors)
    try:
        import streamlit as st
        value = st.secrets.get(key)
        if value is not None:
            return str(value)
    except Exception:  # noqa: BLE001 – st.secrets may not exist yet
        pass

    # 2. Fall back to environment variable
    value = os.getenv(key)
    if value is not None:
        return value

    # 3. Fall back to hard-coded default (if any)
    return default


# ── Public constants ─────────────────────────────────────────────────────────

GEMINI_API_KEY: str | None = _get_secret("GEMINI_API_KEY")
GEMINI_TEXT_MODEL: str = _get_secret("GEMINI_TEXT_MODEL", "gemini-flash-lite-latest") or "gemini-flash-lite-latest"
GEMINI_IMAGE_MODEL: str = _get_secret("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image") or "gemini-3.1-flash-image"
