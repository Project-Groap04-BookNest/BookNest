# 📚 BookNest

---
## 📅DB-ERD
![alt text](/static/assets/DB_stu2.PNG)

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
| Email    | admin@example.com     |
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

## 🤞 ขั้นตอนแตก branch

```bash
# ตรวจสอบว่าอยู่ main ก่อน
git checkout main

# ดึงอัปเดตจาก origin ให้ชัวร์ก่อนแตก branch
git pull

# แตก branch ใหม่
git checkout -b feat/models-user
```

---

## 📁 Project Structure

```
BookNest/
├── app.py                  # main entry point (สร้าง Flask app, register blueprints)
├── config.py               # config สำหรับ DB + ENV
├── docker-compose.yml      # (ถ้าใช้ docker)
├── mock.py                 # สคริปต์สร้าง mock data
├── requirements.txt        # dependency ทั้งหมด
├── .env                    # เก็บ secret และค่า config
├── .gitignore
├── Readme.md

├── models/                 # ORM models (SQLAlchemy)
│   ├── __init__.py
│   ├── user.py
│   ├── book.py
│   ├── book_categories.py
│   ├── order.py
│   └── order_item.py

├── routes/                 # แยก route ออกมาเป็น Blueprint เป็น class จัดการง่าย หน้า app.py สะอาด
│   ├── ui_routes.py        # route สำหรับ render template (Jinja2) ก็คือระบบ html ของ flask 
│   └── api_routes.py       # route สำหรับ JSON API เวลาเขียน api มาทำในนี้ 

├── static/                 # ไฟล์ static (CSS, JS, รูปภาพ)
│   ├── style.css
│   └── assets/
│       └── (icons, images)

├── templates/              # Jinja2 templates (HTML)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── orders.html
│   ├── manage_books.html
│   └── manage_users.html

├── tests/                  # unit tests เผื่อได้ใช้
│   └── ...
└── venv/                   # virtual environment

---





> Made with 💻 by SIET KMITL ทีม "อาจะยัง"

