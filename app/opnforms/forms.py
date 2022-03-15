from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField,\
    StringField, BooleanField, HiddenField, DateField
from wtforms.validators import DataRequired
from flask_admin.form.widgets import Select2Widget, DatePickerWidget
# from wtforms.fields.html5 import DateField


class AAPFilterForm(FlaskForm):
    # period = SelectField(validators=[DataRequired()],
        # choices=[])
    date1 = DateField(widget=DatePickerWidget())
    date2 = DateField(format='%Y-%m-%d')
    item = SelectField(validators=[DataRequired()],
        choices=[])
    warehouse = SelectField(validators=[], choices=[], coerce=int)
    submit = SubmitField('Apply')
