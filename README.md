
# SmartSales Insight

A Streamlit-powered AI tool to analyze sales data from Excel/CSV files. It generates smart insights, charts, and downloadable reports using GPT-4.

## Features
- Upload Excel/CSV sales files
- View sales trends & top products
- Get AI-powered business suggestions
- Export PDF reports

## Setup
1. Add your OpenAI API key to `.streamlit/secrets.toml`:
```
[OPENAI_API_KEY]
OPENAI_API_KEY="your-key"
```

2. Run locally:
```
pip install -r requirements.txt
streamlit run app.py
```
