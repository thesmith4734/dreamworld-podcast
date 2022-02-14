from app import db, ma

class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    description = db.Column(db.String(120), index=True)
    s3_foldername = db.Column(db.String(120), index=True)
    s3_bucket = db.Column(db.String(120), default='dreamworld-podcasts', index=True)

    def __repr__(self):
        return '<File {}>'.format(self.title)

class PodcastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Podcast
        load_instance = True