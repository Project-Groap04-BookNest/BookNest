from flask import Flask
from models import db
from config import Config
from dotenv import load_dotenv
# import blueprints ตัว front-end มา 
from routes.ui_routes import ui_bp
# import routes.api_routes
from routes.api_routes import api_bp

import pytest
# โหลด .env ที่นี่ (ก่อนใช้ Config)
load_dotenv()

#end-point ของตัวเว็บ 
def create_app(testing=False , test_db_uri=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # ตั้ง secret key (ใช้สำหรับ session, flash message)
    app.secret_key = "my_booknest_secret"  # หรือไปอ่านจาก .env ก็ได้
    
    
    #เงื่อนไขในการใช้ pytest เข้ามาทำ unit test 
    if testing and test_db_uri:
        app.config["TESTING"] = True
        if test_db_uri:
            app.config["SQLALCHEMY_DATABASE_URI"] = test_db_uri
            app.config["TESTING"] = True
    
    
    
    
        # init DB
    db.init_app(app)
    
     # register blueprints เอาข้อมูล router เข้ามา
    app.register_blueprint(ui_bp)
    
    #register api เอาข้อมูล api เข้ามา 
    app.register_blueprint(api_bp)



    return app


# ระบบ debug ของ flask
if __name__ == "__main__":
    app = create_app()
    app.secret_key = "my_booknest_secret"
    
    
     # 👇 reset database
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        
    app.run(debug=True)
