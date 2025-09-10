# utils.py
import io
import base64
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import speech_recognition as sr
from fpdf import FPDF

DEFAULT_CATEGORIES = ["Food", "Transport", "Housing", "Shopping", "Entertainment", "Other"]

# ---------- Categorization (simple keyword based) ----------
KEYWORDS = {
    "food": ["grocery", "groceries", "food", "restaurant", "eat", "cafe", "coffee"],
    "transport": ["taxi", "uber", "transport", "bus", "train", "gas", "petrol", "car"],
    "housing": ["rent", "mortgage", "utility", "electricity", "water"],
    "shopping": ["shop", "clothes", "shopping", "mall"],
    "entertainment": ["movie", "netflix", "entertain", "game"],
}

def categorize_text(text: str):
    text_lower = text.lower()
    for cat, kw_list in KEYWORDS.items():
        for kw in kw_list:
            if kw in text_lower:
                # map simple keys to display categories
                if cat == "food":
                    return "Food"
                if cat == "transport":
                    return "Transport"
                if cat == "housing":
                    return "Housing"
                if cat == "shopping":
                    return "Shopping"
                if cat == "entertainment":
                    return "Entertainment"
    return "Other"

# ---------- Plot helpers ----------
def pie_expenses(expenses: dict):
    df = pd.DataFrame(list(expenses.items()), columns=["Category", "Amount"])
    fig = px.pie(df, names="Category", values="Amount", hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def bar_summary(income, total_expenses, savings):
    df = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings"],
        "Amount": [income, total_expenses, savings]
    })
    fig = px.bar(df, x="Category", y="Amount", color="Category", text="Amount")
    fig.update_layout(showlegend=False)
    return fig

def investment_line(months, values):
    df = pd.DataFrame({"Month": months, "Value": values})
    fig = px.line(df, x="Month", y="Value", markers=True)
    fig.update_layout(yaxis_title="Value (DA)")
    return fig

# ---------- Forecasting ----------
def simple_forecast(history_values, n_forecast=3):
    """
    history_values: list or 1d array of past months expenses (length >=2 recommended)
    returns forecast array of length n_forecast
    Uses linear regression on indices -> values
    """
    arr = np.array(history_values).reshape(-1, 1)
    if arr.shape[0] < 2:
        # not enough points, repeat last value
        return [float(arr[-1])] * n_forecast
    X = np.arange(len(arr)).reshape(-1, 1)
    model = LinearRegression().fit(X, arr)
    future_X = np.arange(len(arr), len(arr) + n_forecast).reshape(-1, 1)
    preds = model.predict(future_X).flatten().tolist()
    return [float(max(0, p)) for p in preds]

# ---------- Transcription ----------
def transcribe_audio_file(uploaded_file):
    """
    uploaded_file: a BytesIO-like or streamlit UploadedFile
    returns: transcription text or error string
    """
    r = sr.Recognizer()
    try:
        # Save bytes to temporary WAV in memory if needed
        audio_bytes = uploaded_file.read()
        audio_stream = io.BytesIO(audio_bytes)
        # Use SpeechRecognition AudioFile which accepts filename-like object in recent versions
        with sr.AudioFile(audio_stream) as source:
            audio = r.record(source)
        # Use Google's free API (requires internet). If offline desired, user must install pocketsphinx
        try:
            text = r.recognize_google(audio, language="en-US")
            return text
        except sr.RequestError:
            # API unreachable
            return "ERROR: Speech recognition service unavailable."
        except sr.UnknownValueError:
            return "ERROR: Could not understand audio."
    except Exception as e:
        return f"ERROR: {e}"

# ---------- Exports ----------
def df_to_excel_bytes(df: pd.DataFrame):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="report")
    return output.getvalue()

def df_to_csv_bytes(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')

def create_pdf_report(summary_text: str, charts_bytes_list: list = None):
    """
    summary_text: plain text summary
    charts_bytes_list: optional list of PNG bytes for small images
    returns: PDF bytes
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, summary_text)
    if charts_bytes_list:
        for idx, png in enumerate(charts_bytes_list):
            try:
                # write image from bytes by saving to tmp in-memory file
                image_stream = io.BytesIO(png)
                image_stream.seek(0)
                fname = f"/tmp/tmp_chart_{idx}.png"
                with open(fname, "wb") as f:
                    f.write(png)
                pdf.add_page()
                pdf.image(fname, x=10, y=20, w=180)
            except Exception:
                continue
    return pdf.output(dest='S').encode('latin-1')
