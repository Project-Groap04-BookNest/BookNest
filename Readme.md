# 📚 BookNest

---

## 🛠 Tech Stack

- 🐍 Python 3.1xx
- 🔥 Flask (Backend API Framework)
- 🐘 PostgreSQL (Database)
- 🐳 Docker (Containerize DB)
- 🧰 SQLAlchemy (ORM)
- 🎛️ pgAdmin (GUI DB Tool)

---

## 🚀 Project Purpose

"BookNest" is an online bookstore system where users can:

- 🛒 Browse & order books
- 📦 Stock keeper manage inventory
- 🛡 Admin manage user roles and access

---

## 📦 Installation & Usage (สำหรับเพื่อนในทีม)

### 1️⃣ Clone project & install Python packages

```bash
git clone https://github.com/Project-Groap04-BookNest/BookNest
cd booknest
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ ตั้งค่า `.env`

สร้าง `.env` จาก เอาจาก discord



### 3️⃣ Start PostgreSQL + pgAdmin via Docker

```bash
docker compose up -d
```

### 4️⃣ Seed mock data (users + books)

```bash
python mock.py
```

### 5️⃣ Run Flask server

```bash
python -m flask --app app.py --debug run

```

### 6️⃣ Access the app

- API base: `http://localhost:5000`
- pgAdmin: `http://localhost:5050`

---

## 🧠 pgAdmin Setup Guide

### 🛠 Login

| Field    | Value                 |
| -------- | --------------------- |
| Email    | admin\@booknest.local |
| Password | admin1234             |

### 🔌 Connect DB (ครั้งแรก)

- Host: `db`
- Port: `5432`
- Username: ตาม `.env`
- Password: ตาม `.env`
- DB name: `booknest`

---

## 🧪 Testing

- ทดสอบด้วย Pytest ได้ใน `/tests`

```bash
pytest tests/
```

---

## 📁 Project Structure

```
booknest/
├── app.py
├── mock.py
├── docker-compose.yml
├── requirements.txt
├── .env / .env.example
├── /models
│   ├── user.py, book.py, order.py, order_item.py
├── /static
│   └── uploads/ (book images)
├── /templates
│   └── Jinja2 HTML templates
├── /tests
└── /venv
```

---





> Made with 💻 by SIET KMITL ทีม "อาจะยัง"

