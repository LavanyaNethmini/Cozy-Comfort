from flask import Flask
from seller_service import seller_bp
from notification_service import notification_bp
from distributor_service import distributor_bp

app = Flask(__name__)

app.register_blueprint(seller_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(distributor_bp)
pp.register_blueprint(auth_bp)
app.register_blueprint(manufacture_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.run()
