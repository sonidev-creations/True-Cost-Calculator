<p align="center">
  <img src="https://raw.githubusercontent.com/sonidev-creations/true-cost-calculator/master/assets/screenshot.png.png" width="700"/>
</p>

# 🌍 True Cost Calculator using Agentic AI

<br>

True Cost Calculator is an Agentic AI-based system that helps users estimate the real cost of international purchases by analyzing product price, import duty, shipping charges, and currency conversion. It provides an intelligent breakdown to help users make better purchasing decisions.

---

## 🚀 Features

- 🤖 AI-powered cost calculation using Agentic AI  
- 💱 Real-time currency conversion support  
- 🧾 Import duty and tax estimation  
- 📊 Interactive Streamlit dashboard  
- 📚 History tracking using SQLite database  
- ⚡ Fast backend API with Flask  

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Backend:** Flask  
- **AI Framework:** Groq(Langchain)  
- **Database:** SQLite (`truecost.db`)  
- **Frontend/UI:** Streamlit  
- **Other Tools:** Web scraping, REST APIs  

---

## 📁 Project Structure

```
true-cost-calculator/
├── assets/
│   └── screenshot.png
│
├── backend/
│   ├── app.py
│   ├── main.py
│   ├── server.py
│   ├── scraper.py
│   ├── inspect_db.py
│   ├── requirements.txt
│   ├── truecost.db
│   ├── .env
│   ├── env.example
│   │
│   ├── services/
│   │   └── ai_agent.py
│   │
│   ├── instance/
│   └── __pycache__/
│
├── frontend/
│   ├── app.py
│   ├── .streamlit/
│   │   └── config.toml
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── agent_log.py
│   │   ├── header.py
│   │   ├── input_form.py
│   │   ├── results.py
│   │   ├── sidebar.py
│   │   └── styles.py
│   │
│   └── __pycache__/
│
├── .venv/
├── README.md
├── requirements.txt
├── .gitignore
```

---

## ⚙️ How It Works

1. User enters product price and country  
2. AI agent analyzes cost factors (tax, duty, shipping)  
3. Backend processes data and calculates total cost  
4. Currency conversion is applied  
5. Final cost is displayed with detailed breakdown  

---

## ▶️ Running Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/sonidev-creations/true-cost-calculator.git
cd true-cost-calculator
```

### 2️⃣ Create and activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables
Create a `.env` file inside `backend/`:

```
GROQ_API_KEY=your_api_key
```

---

### 5️⃣ Run Backend
```bash
cd backend
python app.py
```

👉 Runs on: http://localhost:5000  

---

### 6️⃣ Run Frontend
```bash
cd ..
streamlit run frontend/app.py
```

---

## 👨‍💻 Developer

Made with ❤️ by **Soni P**  
📧 iamsoni.btech@gmail.com  
🔗 https://www.linkedin.com/in/sonipandian/
