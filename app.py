from flask import Flask ,render_template , request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os 


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
     if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # เช็คจาก database / session
        return redirect(url_for("index"))
     return render_template('login.html')
 
@app.route('/orders')
def orders():
    return render_template("orders.html")

if __name__ == '__main__':
    app.run(debug=True)