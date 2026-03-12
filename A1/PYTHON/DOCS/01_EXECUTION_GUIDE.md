# Python Tool Execution Guide

This guide will walk you through setting up Python and executing the Scientometric pipeline.

## 1. Prerequisites

You need to have Python installed on your system (Preferably Python 3.10+). Ensure that the option to "Add Python to PATH" is checked during installation if you are on Windows.

## 2. Set Up the Virtual Environment (venv)

Opening a terminal (Command Prompt, PowerShell, or Git Bash) inside the `TOOL` folder.

1. Create the virtual environment:

   ```bash
   python -m venv test_env
   ```

2. Activate the virtual environment:
   - **Windows (PowerShell):** `.\test_env\Scripts\Activate.ps1`
   - **Windows (CMD):** `.\test_env\Scripts\activate.bat`
   - **Mac/Linux:** `source test_env/bin/activate`

## 3. Install Requirements

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

*(These include `pandas`, `requests`, `python-dotenv`, and `openai`)*

## 4. Configuration

1. Unhide/Rename `.env_sample` to `.env`.
2. Open the `.env` file and insert your API keys as detailed in the `02_API_KEYS_GUIDE.md`.

## 5. Input Data Format

Place a `.csv` file in the `data/` folder (or adjust the path in `main.py`). The pipeline expects the CSV file to contain **at least** a column explicitly named `DOI` containing the DOIs you want to scrape (e.g., `10.1007/s11030-021-10217-3`).

## 6. Execution

Run the orchestrator:

```bash
python main.py
```

The terminal will log out the status of each node (OpenAlex, PubMed, Scopus, etc.) as it queries them. The final merged dataset will be saved automatically as `data/MASTER_AUTHOR_TABLE.csv`.
