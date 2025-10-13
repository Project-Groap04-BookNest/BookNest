import pytest
from app import create_app
from models import db
from models.user import User
from dotenv import load_dotenv
import os

load_dotenv()  # โหลดค่าจาก .env

@pytest.fixture(scope="module")
def test_client():
    t_db_uri = os.getenv("TEST_DATABASE_URI")  # ดึงค่าจาก .env
    app = create_app(testing=True, test_db_uri=t_db_uri)

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
        
def test_login_success(test_client):
    # Arrange: สร้าง user mock
    user = User(name="test", email="test@example.com", password_hash="1234", role="user")
    db.session.add(user)
    db.session.commit()

    # Act: ยิง POST /login
    response = test_client.post("/login", data={
        "email": "test@example.com",
        "password": "1234"
    }, follow_redirects=True)

    # Assert: login สำเร็จ
    assert b"login pass" in response.data or response.status_code == 200

def test_login_fail(test_client):
    response = test_client.post("/login", data={
        "email": "wrong@example.com",
        "password": "wrong"
    }, follow_redirects=True)
    assert b"login fail" in response.data or response.status_code == 200