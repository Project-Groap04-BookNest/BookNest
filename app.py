from flask import Flask
from models import db
from config import Config
from dotenv import load_dotenv
# import blueprints ตัว front-end มา 
from routes.ui_routes import ui_bp
# import routes.api_routes

# โหลด .env ที่นี่ (ก่อนใช้ Config)
load_dotenv()

#end-point ของตัวเว็บ 
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
     # register blueprints
    app.register_blueprint(ui_bp)



    return app


# ระบบ debug ของ flask
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
