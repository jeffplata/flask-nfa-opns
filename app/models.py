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
    region_name = db.Column(db.String(80))
    alternate_name = db.Column(db.String(80))
    
    def __repr__(self):
        return '<Region %r>' % (self.region_name)

class Branch(Base):
    __tablename__ = "branch"
    branch_name = db.Column(db.String(80))
    region_id = db.Column(db.Integer(), db.ForeignKey('region.id', ondelete='CASCADE'))
    
    def __repr__(self):
        return '<Branch %r>' % (self.branch_name)

class Warehouse(Base):
    __tablename__ = "warehouse"
    warehouse_name = db.Column(db.String(80))
    warehouse_code = db.Column(db.String(20))