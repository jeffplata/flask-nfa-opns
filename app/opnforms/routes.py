from app.opnforms import bp
from flask import render_template

from .forms import AAPFilterForm
from app import db
from app.models import AAP


# from flask_table import Table, Col
PERIODS_ = [('today', 'Today'), ('yesterday', 'Yesterday'),\
    ('thisweek', 'This week'), ('lastweek', 'Last week'),\
    ('thisquarter', 'This quarter'), ('lastquarter', 'Last quarter'),\
    ('thisyear', 'This Year'), ('lastyear', 'Last year')] 

@bp.route('/aap', methods=['GET', 'POST'])
def list_aap():
    items = AAP.query.all()
    form = AAPFilterForm()
    form.period.choices = PERIODS_
    form.item.choices = [('WD1', 'WD1'), ('WD2', 'WD2'), ('PD1', 'PD1'), ('PD3', 'PD3')]
    form.warehouse.choices = [(1, 'Alang-alang GID 1'), (2, 'Alang-alang GID 2')]
    return render_template('pages/listAAP.html', items=items, form=form)
