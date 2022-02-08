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

    def __repr__(self):
        return '<Warehouse %r>' % (self.warehouse_name)

class Container(Base):
    __tablename__ = "container"
    cont_name = db.Column(db.String(80))
    weight = db.Column(db.Numeric(8,2))

    def __repr__(self):
        return '<Container %r>' % (self.cont_name)

class Commodity(Base):
    __tablename__ = "commodity"
    comm_name = db.Column(db.String(80))
    is_cereal = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return '<Commodity %r>' % (self.comm_name)
