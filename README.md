# Web Scraper Bot

A Streamlit app that launches a Selenium Chrome browser to scrape web pages, extract text (optionally focusing on specific HTML tags), surface prompt-aligned snippets, and run sentiment analysis with TextBlob. Styling is tuned for a dark theme.
<img width="1919" height="917" alt="Screenshot 2026-01-20 210824" src="https://github.com/user-attachments/assets/94b77c20-7661-4d64-b779-fa10852f98ac" />


## Features
- Headless or headed Chrome via Selenium (uses webdriver-manager to fetch ChromeDriver automatically)
- Scrape whole pages or specific element tags (p, div, span, a, h1/h2/h3, article, section, button)
- Prompt-aligned snippets: pulls the sentences that best match your prompt
- Sentiment analysis with polarity, subjectivity, and neutral confidence
- Streamlit UI with tabs for sentiment, prompt matches, content preview, and details
<img width="1919" height="886" alt="Screenshot 2026-01-20 205601" src="https://github.com/user-attachments/assets/3c9550ff-732d-468e-8901-8981d7b18ab0" />

## Prerequisites
- Python 3.9+
- Google Chrome installed (webdriver-manager will match your Chrome)
- Windows (current tested environment), but should work on macOS/Linux with Chrome available

## Installation
From the `Web-Scrapper` folder:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install --upgrade pip
pip install streamlit selenium webdriver-manager textblob beautifulsoup4
# Optional: speed up TextBlob downloads by pre-downloading corpora if needed
```

If TextBlob complains about missing corpora (rare for polarity/subjectivity), run:
```bash
python -m textblob.download_corpora
```

## Running the app
From the `Web-Scrapper` folder with the venv activated:
```bash
streamlit run webapp.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## Usage
1) Enter a target URL.
2) Optionally enter a prompt (e.g., "pricing and refund policy").
3) Choose scrape mode: Entire Page or Specific Elements (pick a tag if specific).
4) Click "Scrape & Analyze".
5) Review tabs:
   - Sentiment Analysis: overall sentiment, polarity/subjectivity, charts.
   - Prompt Matches: snippets most aligned with your prompt.
   - Content Preview: truncated page text.
   - Details: URL, content length, scraping mode, element tag (if used).

## Notes and tips
- If headless mode fails on some sites, uncheck Headless Mode to let Chrome render fully.
- Some sites block automation; consider adding waits or using more specific element tags.
- The prompt matcher is keyword-based; clearer, specific prompts yield better snippets.
- For large or dynamic pages, increase page load wait time inside `scrape_and_analyze` if needed.

## Project structure
```
Web-Scrapper/
  bot.py         # Selenium wrapper, scraping, prompt matching, sentiment
  webapp.py      # Streamlit UI
  README.md
```
