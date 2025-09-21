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
# 📘 วิธีสร้าง API และเชื่อมเข้ากับหน้าเว็บใน Flask

โปรเจคนี้ใช้ **Flask + SQLAlchemy + Jinja2**  
แนวคิดคือ
1. ทำ **API** สำหรับดึงข้อมูลจาก Database
2. ทำ **UI Route** ที่จะ query DB โดยตรง และส่งข้อมูลไป render ที่หน้า HTML (Jinja2 Template)

---

## 🔹 ก่อนเริ่ม ต้องเข้าใจ Database
- แต่ละหน้าเว็บจะแสดงข้อมูลจาก **Table** ที่อยู่ใน Database  
- เช่น หน้า `manage_books` ต้องดู **ตาราง Book** ใน DB ก่อน ว่ามี column อะไรบ้าง  

# 📂 Database Schema (BookNest)

## 1. User
เก็บข้อมูลผู้ใช้ระบบ

| Column        | Type        | Description                      |
|---------------|-------------|----------------------------------|
| id            | Integer PK  | รหัสผู้ใช้                       |
| name          | String      | ชื่อ                              |
| email         | String (UQ) | อีเมล (unique)                   |
| password_hash | String      | รหัสผ่าน (เก็บ hash)             |
| role          | String/Enum | บทบาท (user, stock_keeper, admin)|

---

## 2. BookCategory
หมวดหมู่ของหนังสือ

| Column | Type       | Description   |
|--------|------------|---------------|
| id     | Integer PK | รหัสหมวดหมู่ |
| name   | String     | ชื่อหมวดหมู่ |

---

## 3. Book
เก็บรายละเอียดหนังสือ

| Column         | Type        | Description              |
|----------------|-------------|--------------------------|
| id             | Integer PK  | รหัสหนังสือ              |
| title          | String      | ชื่อหนังสือ             |
| author         | String      | ผู้เขียน                 |
| price          | Decimal     | ราคาหนังสือ             |
| stock_quantity | Integer     | จำนวนคงเหลือ            |
| image_path     | String      | path รูปภาพ              |
| category_id    | FK          | อ้างอิง → BookCategory.id|

---

## 4. Order
เก็บข้อมูลออเดอร์

| Column     | Type        | Description                        |
|------------|-------------|------------------------------------|
| id         | Integer PK  | รหัสออเดอร์                        |
| user_id    | FK          | อ้างอิง → User.id (ใครสั่งซื้อ)     |
| status     | String/Enum | สถานะ (pending, paid, shipped)    |
| created_at | DateTime    | เวลาในการสร้างออเดอร์              |

---

## 5. OrderItem
เก็บรายละเอียดสินค้าในออเดอร์ (M:N ระหว่าง Order และ Book)

| Column   | Type        | Description                     |
|----------|-------------|---------------------------------|
| id       | Integer PK  | รหัส row                        |
| order_id | FK          | อ้างอิง → Order.id               |
| book_id  | FK          | อ้างอิง → Book.id                |
| quantity | Integer     | จำนวนที่สั่งซื้อ                 |
| price    | Decimal     | ราคาต่อหน่วย (ตอนสั่งซื้อ)      |

---

# 🔗 ERD (ความสัมพันธ์)

- **User (1) → (M) Order**  
- **Order (1) → (M) OrderItem**  
- **Book (1) → (M) OrderItem**  
- **BookCategory (1) → (M) Book**



# 🌐 การทำงานของ API และการเชื่อมเข้าหน้าเว็บ (Flask + Jinja2)

## 🌐 API Routes

### `GET /api/get_books`
- ดึงข้อมูลหนังสือทั้งหมดจาก Database  
- ส่งกลับเป็น JSON  

**Response (ตัวอย่าง):**
```json
[
  {
    "id": 1,
    "title": "Python 101",
    "author": "Guido",
    "price": "299.00",
    "stock_quantity": 5
  },
  {
    "id": 2,
    "title": "Flask Mastery",
    "author": "Miguel",
    "price": "450.00",
    "stock_quantity": 10
  }
]
```

# 🖥️ UI Routes

หน้าเว็บ `/manage_books` จะ query ข้อมูลจากตาราง **Book** ใน DB โดยตรง  
แล้วส่งข้อมูลไปยัง **Jinja2 Template** เพื่อ render หน้าเว็บ  

---

## 🎨 Template (Jinja2)

ไฟล์: `templates/manage_books.html`  

ใช้ `{% for book in books %}` เพื่อ loop แสดงข้อมูล  
โดยดึง column จาก table **Book** เช่น `title`, `author`, `stock_quantity`, `image_path`  

**ตัวอย่างการ render:**

```jinja2
{% for book in books %}
  <div class="bg-gray-800 rounded-xl p-3 flex flex-col">
    <img src="{{ url_for('static', filename=book.image_path or 'assets/mock-book01.svg') }}"
         alt="{{ book.title }}"
         class="rounded-lg mb-3">
    <div class="flex flex-col">
      <h2 class="text-white text-lg font-semibold mb-1">{{ book.title }}</h2>
      <p class="text-gray-300 text-sm mb-2">by {{ book.author }}</p>
    </div>
    <div class="flex items-center justify-between bg-black rounded-md px-3 py-1">
      <span class="text-lg text-white">{{ book.stock_quantity }} left</span>
      <button class="bg-gray-900 text-white px-2 py-1 rounded hover:bg-gray-600">+</button>
    </div>
  </div>
{% endfor %}
```

### 🔄 Flow การทำงาน

``` ผู้ใช้เปิดหน้า /manage_books

Flask (UI Route) query ข้อมูลจากตาราง Book

ส่งตัวแปร books ไปที่ Jinja2 Template

Template ใช้ {% for book in books %} loop แล้ว render HTML แสดงผล

✅ สรุปสำหรับมือใหม่

API Routes (routes/api_routes.py)
ใช้ส่งข้อมูลเป็น JSON (เหมาะสำหรับ front-end แยก หรือ mobile app)

UI Routes (routes/ui_routes.py)
ใช้ query DB และ render HTML โดยตรงผ่าน Jinja2

Database
ต้องตรวจสอบตาราง (เช่น Book) ว่ามี column อะไรบ้าง → ถึงจะเลือกมาแสดงผลได้ถูก

app.py
เป็นศูนย์กลาง:

โหลด config

init database

register blueprints (ทั้ง API และ UI)
```





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

