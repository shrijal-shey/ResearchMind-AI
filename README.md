# ResearchMind AI

A Streamlit research assistant that searches the web, gathers source material, and uses Gemini to write and review a report.

## Requirements

- Python 3.11 or newer
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Setup

1. Clone this repository and open a terminal in the project folder.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your Gemini API key to `GOOGLE_API_KEY`.
5. Start the app:

   ```powershell
   streamlit run app.py
   ```

Each user should provide their own API key in their local `.env` file. Never commit `.env`; it is excluded by `.gitignore`.
