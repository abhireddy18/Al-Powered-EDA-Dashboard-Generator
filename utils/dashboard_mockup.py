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
        x = 28 + (index % 2) * 300
        y = 106 + (index // 2) * 140
        color = palette[index % len(palette)]
        metrics.append(
            f'''
            <g transform="translate({x},{y})">
              <rect width="250" height="108" rx="18" fill="#141a2b" stroke="rgba(255,255,255,0.08)"/>
              <rect x="14" y="16" width="48" height="48" rx="12" fill="{color}" opacity="0.22"/>
              <text x="20" y="38" font-size="18" fill="#d6def7" font-weight="600">{label}</text>
              <text x="20" y="70" font-size="26" fill="#f7f9ff" font-weight="700">{value}</text>
              <text x="20" y="92" font-size="12" fill="{color}" font-weight="600">{delta}</text>
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
    <svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720" role="img" aria-label="Dashboard concept mockup" class="dashboard-mockup">
      <defs>
        <linearGradient id="bg" x1="0" x2="1">
          <stop offset="0%" stop-color="#0b1020"/>
          <stop offset="100%" stop-color="#141d35"/>
        </linearGradient>
        <linearGradient id="panel" x1="0" x2="1">
          <stop offset="0%" stop-color="#17213b"/>
          <stop offset="100%" stop-color="#10182d"/>
        </linearGradient>
      </defs>
      <rect width="960" height="720" fill="url(#bg)"/>
      <rect x="24" y="24" width="912" height="672" rx="28" fill="url(#panel)" stroke="rgba(255,255,255,0.08)"/>
      <rect x="56" y="54" width="160" height="38" rx="12" fill="#202b48"/>
      <text x="82" y="80" font-size="20" fill="#7dd3fc" font-weight="700">ApexFlow</text>
      <text x="257" y="80" font-size="14" fill="#98a7d9">Overview</text>
      <text x="600" y="80" font-size="14" fill="#98a7d9">Revenue</text>
      <text x="760" y="80" font-size="14" fill="#98a7d9">Insights</text>
      <text x="820" y="80" font-size="14" fill="#98a7d9">Export</text>
      <text x="36" y="118" font-size="26" fill="#f5f7ff" font-weight="700">Executive dashboard</text>
      <text x="36" y="146" font-size="14" fill="#98a7d9">Design concept • no image tokens used</text>
      {''.join(metrics)}
      <rect x="626" y="110" width="264" height="240" rx="18" fill="#111b2d" stroke="rgba(255,255,255,0.08)"/>
      <text x="650" y="142" font-size="14" fill="#98a7d9">Performance</text>
      <path d="M 650 300 C 690 240, 720 250, 760 220 S 830 160, 860 120" fill="none" stroke="#7dd3fc" stroke-width="4" stroke-linecap="round"/>
      <circle cx="760" cy="220" r="6" fill="#7dd3fc"/>
      <circle cx="860" cy="120" r="6" fill="#6ee7b7"/>
      <text x="650" y="330" font-size="12" fill="#98a7d9">Q1</text>
      <text x="760" y="330" font-size="12" fill="#98a7d9">Q2</text>
      <text x="850" y="330" font-size="12" fill="#98a7d9">Q3</text>
      <rect x="34" y="360" width="570" height="210" rx="18" fill="#111b2d" stroke="rgba(255,255,255,0.08)"/>
      <text x="56" y="392" font-size="14" fill="#98a7d9">Trend</text>
      {''.join(mini_bars)}
      <rect x="610" y="380" width="290" height="190" rx="18" fill="#111b2d" stroke="rgba(255,255,255,0.08)"/>
      <text x="634" y="412" font-size="14" fill="#98a7d9">Highlights</text>
      {''.join(insight_items)}
      {summary_html}
    </svg>
    '''.strip()
