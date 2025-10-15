## Sales Outreach AI Tool

A lightweight AI-assisted sales outreach workflows.

### Features
- **Starter entrypoint**: `main.py`
- **Dependency scaffold**: `requirements.txt` includes typical libraries for AI apps (`openai`, `gradio`, `pypdf`, `requests`, `python-dotenv`).
- **Modern Python**: Targets Python 3.12+ via `pyproject.toml`.

### Requirements
- **Python**: 3.12 or newer
- **OS**: Windows, macOS, or Linux

### Quickstart
1) Create and activate a virtual environment
```
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) (Optional) Configure environment variables
If you plan to call the OpenAI APIs, create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key
# Optional
# OPENAI_BASE_URL=https://api.openai.com/v1
```

4) Run the app
```
python main.py
```

You should see:
```

```

### Project Structure
```
sales-outreach-ai-tool/
├─ main.py               # Entry script
├─ requirements.txt      # Python dependencies
├─ pyproject.toml        # Project metadata (Python 3.12+)
└─ README.md             # You are here
```

### Next Steps / Ideas
- Hook up `openai` to generate personalized outreach copy from lead data.
- Add a small `gradio` UI for drafting and reviewing messages.
- Parse lead lists or collateral with `pypdf` and summarize with LLMs.
- Add unit tests and CI.

### Troubleshooting
- If `python` points to Python 3.11 or lower, explicitly use `py -3.12` on Windows or install Python 3.12+.
- If imports fail, ensure your virtual environment is activated before running commands.

### License
TBD


