from app import db
# from user_models import Base

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

class Region(Base):
	__tablename__ = "region"
	region_name = db.Column(db.String(128))
	alternate_name = db.Column(db.String(128))
