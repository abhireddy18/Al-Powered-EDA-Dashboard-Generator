# AI-Powered EDA & Dashboard Generator

GitHub repository: `Al-Powered-EDA-Dashboard-Generator`

An intelligent exploratory data analysis tool that uses **Google Gemini** to decide _what_ to analyse, while computing every number from the real data in Python — **zero hallucinated numbers**.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Smart Analysis** | Upload CSV/Excel → Gemini designs KPIs, charts & insights |
| **No Hallucinated Numbers** | Every KPI and chart is computed from real data via pandas/Plotly |
| **Interactive Charts** | Dark-themed Plotly charts with zoom, hover, and export |
| **10 Chart Types** | Bar, line, scatter, histogram, box, pie, heatmap, treemap, sunburst, funnel |
| **Dynamic Filters** | Sidebar filter widgets auto-generated from your data |
| **KPI Deltas** | Up/down indicators comparing mean vs median, etc. |
| **Tabbed Layout** | Clean result organisation: KPIs → Charts → Insights → Code → Image |
| **Auto-Retry** | Exponential backoff on transient API errors (429/500/502/503) |
| **Analysis Caching** | Same prompt on the same file returns instantly without re-calling Gemini |
| **Smart Date Handling** | Auto-detects date columns and resamples line charts appropriately |
| **EDA Code Export** | One-click Python script generation (pandas + matplotlib) |
| **Dashboard Mockup** | AI-generated stylised dashboard image (Gemini image model) |

---

## 📁 Project Structure

```
eda_streamlit_app/
├── app.py                          # Streamlit UI + orchestration
├── config.py                       # API key & model config (secrets + .env)
├── requirements.txt
├── .env.example                    # Template for local development
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example        # Template for Streamlit Cloud
├── utils/
│   ├── __init__.py
│   ├── data_loader.py              # File loading, date parsing, profiling
│   ├── prompts.py                  # Prompt templates for Gemini tasks
│   ├── gemini_client.py            # Gemini client with retry + profile trimming
│   ├── eda_engine.py               # Validation, KPIs, charts (10 types)
│   └── filters.py                  # Dynamic sidebar filter builder
└── outputs/
    ├── generated_code/             # Saved EDA scripts (gitignored)
    └── generated_images/           # Saved dashboard images (gitignored)
```

---

## 🚀 Local Setup

### 1. Install Python dependencies

Use Python 3.10 or newer. Open a terminal in the project folder (the folder containing `app.py`) and run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Configure API key

Copy `.env.example` to `.env` and add your [Google AI Studio API key](https://aistudio.google.com/apikey). Do not overwrite an existing `.env` file.

```powershell
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY=your-key
```

### 3. Run

```powershell
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`. Uploading and exploring data works without an API key; Gemini-powered analysis and generation require `GEMINI_API_KEY`.

---

## ☁️ Streamlit Community Cloud Deployment

1. **Push to GitHub** — commit the repo (`.env` is gitignored, your key stays safe).
2. **Create a new app** on [share.streamlit.io](https://share.streamlit.io/).
3. **Add your secret** in the app's **Settings → Secrets** panel:

   ```toml
    GEMINI_API_KEY = "your-gemini-api-key-here"
   ```

4. Deploy — `config.py` reads `st.secrets` first, so no code changes are needed.

---

## 🔒 How "No Hallucinated Numbers" Works

```
User request  ──►  Build data profile (pandas)
                        │
                        ▼
               Send profile to Gemini  ──►  Gemini returns a PLAN (JSON)
                                               │
                                               ▼
                                     Validate plan in Python
                                     (drop bad columns / types)
                                               │
                                               ▼
                                     Compute KPIs  ← pandas (real data)
                                     Build charts  ← Plotly  (real data)
                                               │
                                               ▼
                                     Display results in Streamlit
```

Gemini **never** computes or states a numeric value. It only decides _what_ to compute. Every number on screen comes from `pandas` running against the real DataFrame.

---

## 🔄 Resilience Features

- **Auto-retry** with exponential backoff (1s → 2s → 4s) for status codes 429, 500, 502, 503, 504
- **Token budget guard** automatically trims large profiles to prevent context-window overflows
- **Malformed JSON handling** — catches JSONDecodeError and prompts the user to retry
- **Column validation** — silently drops any Gemini suggestion referencing non-existent columns
- **Analysis caching** — re-running the same prompt on the same file uses cached results

---

## 📝 License

MIT
