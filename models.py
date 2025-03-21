from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class VesterAi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    slide_title = db.Column(db.String(255), nullable=False)
    slide_content = db.Column(db.db.Text, nullable=False)
    metadata = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f'<VesterAi {self.filename}'
