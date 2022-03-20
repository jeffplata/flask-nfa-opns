from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField,\
    StringField, BooleanField, HiddenField, DateField,\
    IntegerField, DecimalField, FormField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from flask_admin.form.widgets import Select2Widget
# from wtforms.fields.html5 import DateField


class AAPFilterForm(FlaskForm):
    date1 = DateField(format="%m/%d/%Y")
    date2 = DateField(format="%m/%d/%Y")
    item = SelectField(validators=[DataRequired()],
        choices=[], widget=Select2Widget())
    warehouse = SelectField(validators=[], choices=[], coerce=int)
    submit = SubmitField('Apply')

class DocBaseForm(FlaskForm):
    doc_date = DateField('Date', format="%m/%d/%Y")
    number = StringField('Number')

class AAPForm(FlaskForm):
    basic_data = FormField(DocBaseForm)
    customer = StringField('Customer')
    item_id = QuerySelectField('Item', get_label='item_name')
    bags = IntegerField('Bags')
    net_kg_qty = DecimalField('Net kg/ Quantity')
    unit_sp = DecimalField('Unit Price')
    amount = DecimalField('Total Amount')
    check_no = StringField('Check No.')
    warehouse_id = QuerySelectField('Warehouse', get_label='warehouse_name')

    # customer = db.Column(db.String(255))
    # item_id = db.Column(db.Integer(), db.ForeignKey('item.id', ondelete='CASCADE'))
    # bags = db.Column(db.Integer())
    # net_kg_qty = db.Column(db.Numeric(15,2))
    # unit_sp = db.Column(db.Numeric(15,2))
    # amount = db.Column(db.Numeric(15,2))
    # check_no = db.Column(db.String(40))
    # warehouse_id = db.Column(db.Integer(), db.ForeignKey('warehouse.id', ondelete='CASCADE'))
    # prepared_by = db.Column(db.String(80))
    # approved_by = db.Column(db.String(80))