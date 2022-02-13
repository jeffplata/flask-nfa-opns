from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField,\
    StringField, BooleanField, HiddenField
from wtforms.validators import DataRequired
from flask_admin.form.widgets import Select2Widget

class AAPFilterForm(FlaskForm):
    period = SelectField(validators=[DataRequired()],
        choices=[])
    item = SelectField(validators=[DataRequired()],
        choices=[])
    warehouse = SelectField(validators=[], choices=[])
    submit = SubmitField('Apply')
