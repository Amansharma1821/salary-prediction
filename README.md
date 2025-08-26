# Salary Prediction App On Docker

## Streamlit App

### Setup

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure either `SalaryModel.pkl` exists (run `python Model.py` to generate it) or `Salary_Data.csv` is present so the app can train on first run.

### Run

```bash
streamlit run streamlit_app.py
```

Open the provided local URL in your browser to use the UI.

## Docker Deployment

### Build

```bash
docker build -t salary-prediction-streamlit .
```

### Run

```bash
docker run --rm -p 8501:8501 \
  -v %cd%:/app \
  salary-prediction-streamlit
```

Then open `http://localhost:8501`.

Notes:
- The volume mount keeps your local `SalaryModel.pkl`/`Salary_Data.csv` visible inside the container.
- On macOS/Linux replace `%cd%` with `$(pwd)`.
