from flask import Flask ,render_template , request, redirect, url_for
import os 
from models import db
from models.user import User
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}"
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password_hash=password).first()
        if user:
            return redirect(url_for("index"))
        else:
            return render_template('login.html', error="rahat mai tug")
    return render_template('login.html')
 
@app.route('/orders')
def orders():
    return render_template("orders.html")

@app.route('/manage_books')
def manage_books():
    return render_template("manage_books.html")

@app.route('/manage_users')
def manage_users():
    return render_template("manage_user.html")

if __name__ == '__main__':
    app.run(debug=True)