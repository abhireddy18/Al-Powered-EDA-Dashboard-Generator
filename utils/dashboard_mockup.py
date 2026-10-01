"""No-token dashboard concept renderer for the EDA app."""

from __future__ import annotations


def _escape_svg_text(value: object) -> str:
    """Return safe text for inline SVG content."""
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_dashboard_mockup_svg(kpi_results: list[dict], insights: list[str]) -> str:
    """Build a styled dashboard concept as SVG without consuming Gemini image tokens."""
    metrics = []
    palette = ["#6ee7b7", "#7dd3fc", "#c4b5fd", "#fbbf24"]

    for index, item in enumerate(kpi_results[:4]):
        label = _escape_svg_text(item.get("label") or item.get("metric") or f"Metric {index + 1}")
        value = _escape_svg_text(item.get("value") or item.get("metric_value") or "—")
        delta = _escape_svg_text(item.get("delta") or item.get("change") or "")
        x = 240 + (index % 2) * 180
        y = 110 + (index // 2) * 110
        color = palette[index % len(palette)]
        metrics.append(
            f'''
            <g transform="translate({x},{y})">
              <rect width="160" height="94" rx="18" fill="#121e33" stroke="rgba(255,255,255,0.07)"/>
              <rect x="14" y="16" width="38" height="38" rx="12" fill="{color}" opacity="0.2"/>
              <text x="18" y="36" font-size="12" fill="#dfe7ff" font-weight="600">{label}</text>
              <text x="18" y="66" font-size="22" fill="#f7f9ff" font-weight="700">{value}</text>
              <text x="18" y="82" font-size="11" fill="{color}" font-weight="600">{delta}</text>
            </g>
            '''
        )

    mini_bars = []
    for idx in range(12):
        height = 42 + ((idx * 11) % 40)
        x = 36 + idx * 18
        y = 420 - height
        mini_bars.append(
            f'<rect x="{x}" y="{y}" width="10" height="{height}" rx="4" fill="#4cc9f0" opacity="{0.35 + (idx % 4) * 0.12}"/>'
        )

    insight_items = []
    insight_lines = insights or ["Key drivers and momentum are trending in the right direction."]
    for idx, bullet in enumerate(insight_lines[:3]):
        clean_bullet = _escape_svg_text(bullet)
        insight_items.append(
            f'''
            <g transform="translate(40,{470 + idx * 54})">
              <circle cx="8" cy="8" r="6" fill="#7dd3fc"/>
              <text x="24" y="14" font-size="16" fill="#e5ecff">{clean_bullet}</text>
            </g>
            '''
        )

    summary_items = ["Revenue trend", "Retention", "Conversion", "Forecast"]
    summary_html = "".join(
        f'<text x="{50 + i * 120}" y="560" font-size="12" fill="#98a7d9">{summary_items[i]}</text>'
        for i in range(len(summary_items))
    )

    return f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720" role="img" aria-label="Webpage dashboard mockup" class="dashboard-mockup">
      <defs>
        <linearGradient id="bg" x1="0" x2="1">
          <stop offset="0%" stop-color="#101827"/>
          <stop offset="100%" stop-color="#0d1527"/>
        </linearGradient>
        <linearGradient id="panel" x1="0" x2="1">
          <stop offset="0%" stop-color="#16233a"/>
          <stop offset="100%" stop-color="#101b2d"/>
        </linearGradient>
        <linearGradient id="soft" x1="0" x2="1">
          <stop offset="0%" stop-color="#1a2a46"/>
          <stop offset="100%" stop-color="#121d34"/>
        </linearGradient>
      </defs>

      <rect width="960" height="720" fill="url(#bg)"/>
      <rect x="24" y="20" width="912" height="680" rx="26" fill="#101828" stroke="rgba(255,255,255,0.08)"/>

      <rect x="40" y="36" width="880" height="44" rx="14" fill="#1a2335"/>
      <circle cx="66" cy="58" r="6" fill="#ff5f57"/>
      <circle cx="84" cy="58" r="6" fill="#febc2e"/>
      <circle cx="102" cy="58" r="6" fill="#28c840"/>
      <rect x="128" y="48" width="330" height="20" rx="10" fill="#0e1729"/>
      <text x="610" y="62" font-size="12" fill="#9fb0d8">analytics.executive-portal.ai</text>

      <rect x="40" y="96" width="160" height="576" rx="18" fill="url(#soft)"/>
      <text x="70" y="130" font-size="24" font-weight="700" fill="#f5f7ff">PulseBoard</text>
      <rect x="62" y="162" width="116" height="32" rx="10" fill="#243358"/>
      <text x="88" y="183" font-size="12" fill="#dce7ff">Overview</text>
      <rect x="62" y="208" width="116" height="32" rx="10" fill="#101b2d"/>
      <text x="87" y="229" font-size="12" fill="#8ea1d2">Revenue</text>
      <rect x="62" y="254" width="116" height="32" rx="10" fill="#101b2d"/>
      <text x="83" y="275" font-size="12" fill="#8ea1d2">Customers</text>
      <rect x="62" y="300" width="116" height="32" rx="10" fill="#101b2d"/>
      <text x="87" y="321" font-size="12" fill="#8ea1d2">Forecast</text>

      <rect x="220" y="104" width="666" height="112" rx="18" fill="#121d32" stroke="rgba(255,255,255,0.06)"/>
      <text x="246" y="138" font-size="28" fill="#f5f7ff" font-weight="700">Executive BI portal</text>
      <text x="246" y="164" font-size="14" fill="#9fb0d8">Premium SaaS dashboard preview • no image tokens used</text>
      <rect x="700" y="120" width="150" height="32" rx="10" fill="#243358"/>
      <text x="734" y="141" font-size="12" fill="#77d7ff">Live metrics</text>

      {''.join(metrics)}

      <rect x="230" y="250" width="392" height="220" rx="18" fill="#111b2d" stroke="rgba(255,255,255,0.06)"/>
      <text x="252" y="280" font-size="12" fill="#9fb0d8">Trend</text>
      {''.join(mini_bars)}
      <rect x="642" y="250" width="224" height="220" rx="18" fill="#111b2d" stroke="rgba(255,255,255,0.06)"/>
      <text x="664" y="280" font-size="12" fill="#9fb0d8">Performance</text>
      <path d="M 664 402 C 694 370, 734 382, 770 344 S 840 286, 846 258" fill="none" stroke="#7dd3fc" stroke-width="4" stroke-linecap="round"/>
      <circle cx="770" cy="344" r="6" fill="#7dd3fc"/>
      <circle cx="846" cy="258" r="6" fill="#6ee7b7"/>
      <text x="670" y="428" font-size="11" fill="#9fb0d8">Jan</text>
      <text x="760" y="428" font-size="11" fill="#9fb0d8">Feb</text>
      <text x="825" y="428" font-size="11" fill="#9fb0d8">Mar</text>

      <rect x="230" y="500" width="636" height="136" rx="18" fill="#111b2d" stroke="rgba(255,255,255,0.06)"/>
      <text x="252" y="530" font-size="12" fill="#9fb0d8">Highlights</text>
      {''.join(insight_items)}
      {summary_html}
    </svg>
    '''.strip()
