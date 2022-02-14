from app import db
# from user_models import Base

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

class BaseForm(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    doc_date = db.Column(db.Date(), default=db.func.current_date())
    number = db.Column(db.String(80))

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
    branch_id = db.Column(db.Integer(), db.ForeignKey('branch.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Warehouse %r>' % (self.warehouse_name)

class Container(Base):
    __tablename__ = "container"
    cont_name = db.Column(db.String(20))
    cont_shortname = db.Column(db.String(20))
    weight = db.Column(db.Numeric(8,2))

    def __repr__(self):
        return '<Container %r>' % (self.cont_name)

class Commodity(Base):
    __tablename__ = "commodity"
    comm_name = db.Column(db.String(80))
    is_cereal = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return '<Commodity %r>' % (self.comm_name)

class Variety(Base):
    __tablename__ = "variety"
    var_name = db.Column(db.String(20))
    commodity_id = db.Column(db.Integer(), db.ForeignKey('commodity.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Variety %r>' % (self.var_name)

class Item(Base):
    __tablename__ = "item"
    item_name = db.Column(db.String(80))
    commodity_id = db.Column(db.Integer(), db.ForeignKey('commodity.id', ondelete='CASCADE'))
    variety_id = db.Column(db.Integer(), db.ForeignKey('variety.id', ondelete='CASCADE'))
    container_id = db.Column(db.Integer(), db.ForeignKey('container.id', ondelete='CASCADE'))
    selling_price = db.Column(db.Numeric(15,2))

# Form models

class AAP(BaseForm):
    customer = db.Column(db.String(255))
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id', ondelete='CASCADE'))
    bags = db.Column(db.Integer())
    net_kg_qty = db.Column(db.Numeric(15,2))
    unit_sp = db.Column(db.Numeric(15,2))
    amount = db.Column(db.Numeric(15,2))
    check_no = db.Column(db.String(40))
    warehouse_id = db.Column(db.Integer(), db.ForeignKey('warehouse.id', ondelete='CASCADE'))
    prepared_by = db.Column(db.String(80))
    approved_by = db.Column(db.String(80))
    