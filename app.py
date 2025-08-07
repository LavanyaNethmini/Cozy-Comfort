from flask import Flask
from flask_cors import CORS

from seller_service import seller_bp
from notification_service import notification_bp
from distributor_service import distributor_bp
from auth_service import auth_bp
from manufacture_service import manufacture_bp
from user_service import user_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(seller_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(distributor_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(manufacture_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run()
