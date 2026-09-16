# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal, local-only AI writing toolkit built with Streamlit and the Gemini API. No database, no
authentication — single user, runs on localhost only. Japanese-language UI.

## Commands

```bash
# First-time setup
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt      # Windows/PowerShell
./.venv/Scripts/pip install -r requirements.txt     # Git Bash

# Run the app
.venv\Scripts\streamlit run app.py                  # Windows/PowerShell
./.venv/Scripts/streamlit run app.py                # Git Bash
```

There is no lint, test, or build tooling in this project — it's a single Streamlit app with no test
suite configured. Verify changes by running the app and exercising the affected page in the browser.

Syntax-check without running the UI:
```bash
./.venv/Scripts/python.exe -m py_compile app.py utils/*.py pages/*.py
```

Port 8501 (Streamlit's default) may already be in use by another local project; pass
`--server.port <N>` to run on an alternate port when testing.

## Architecture

**Multipage Streamlit app.** `app.py` is the home page; each file under `pages/` is a self-contained
feature page, auto-registered in the sidebar nav by Streamlit based on filename (the leading number
controls ordering, the emoji + Japanese text become the nav label and page title). Adding a new
writing tool means adding one new file to `pages/` following the existing pattern — there is no
central router to update.

**`utils/gemini_client.py`** is the only place that talks to the Gemini API (via the `google-genai`
SDK, `google.genai.Client`). All pages call its `generate_text(prompt, system_instruction=None,
temperature=...)`. The API key resolves from `st.session_state["gemini_api_key"]` first, falling back
to the `GEMINI_API_KEY` env var (loaded from `.env` via `python-dotenv`) — the key is never persisted
to disk, only held in the browser session. The Gemini `Client` instance is cached per API key via
`@st.cache_resource`.

**`utils/ui.py`** renders the shared sidebar (API key input, model selector from `MODEL_OPTIONS`,
connection status). Every page calls `render_sidebar()` right after `st.set_page_config(...)` — this
is the convention to follow for any new page.

**Each feature page** follows the same shape: `st.form(...)` for inputs → build a prompt string in
Japanese from the form fields → call `generate_text(...)` inside a `try/except` wrapped in
`st.spinner(...)` → render the result with `st.markdown`/`st.text_area` → offer a `st.download_button`.
Prompts are assembled inline in each page (no shared prompt-template module) — keep new pages
consistent with this pattern rather than introducing a different structure for one page.

Current pages (all under `pages/`, numbered for nav order): ブログ記事作成 (blog), メール返信作成
(email replies), 文章要約 (summarization), 文章校正 (proofreading), 翻訳 (translation), タイトル案生成
(title generation).
