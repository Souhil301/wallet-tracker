# 💰 Wallet Tracking App

A simple and interactive **personal finance tracker** built with **Streamlit**.  
Track your **expenses, savings, and investments** in one place with interactive charts and a clean UI.

---

## Features

- **Expenses Tracking** – input daily/weekly/monthly expenses and visualize spending categories.
- **Savings Goals** – set savings targets and monitor progress.
- **Investments Dashboard** – track portfolio growth and performance with charts.
- **Interactive UI** – powered by Streamlit with Plotly charts.

---

## Live Demo

- **Streamlit**: [https://wallet-tracke.streamlit.app](https://wallet-tracke.streamlit.app/)

---

## Project Structure

```bash
│── app.py
│── pages/
│    ├── 1_Expenses.py
│    ├── 2_Savings.py
│    ├── 3_Investments.py
│── requirements.txt    # Python dependencies
│── .gitignore
│── README.md
```

---

## Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/Souhil301/wallet-tracking.git
cd wallet-tracking
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the frontend (Streamlit)

```bash
streamlit run app.py
```

This runs the dashboard on http://localhost:8501

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss.

---

## License

MIT

© 2025 DSC
