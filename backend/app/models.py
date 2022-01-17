from app import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), index=True)
    path = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<File {}>'.format(self.filename)