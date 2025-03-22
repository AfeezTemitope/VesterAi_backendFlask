from flask import Flask
from dotenv import load_dotenv
from config import Config
from models import db
from urls import setup_routes

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
setup_routes(app)
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
