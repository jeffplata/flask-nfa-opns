from app.opnforms import bp
from flask import render_template

from .forms import AAPFilterForm
from app import db
from app.models import Variety, AAP


# from flask_table import Table, Col
PERIODS_ = [('today', 'Today'), ('yesterday', 'Yesterday'),\
    ('thisweek', 'This week'), ('lastweek', 'Last week'),\
    ('thisquarter', 'This quarter'), ('lastquarter', 'Last quarter'),\
    ('thisyear', 'This Year'), ('lastyear', 'Last year')] 

ITEMS_ = [('WD1', 'WD1'), ('WD2', 'WD2'), ('PD1', 'PD1'), ('PD3', 'PD3')]

WAREHOUSES_ = [(1, 'Alang-alang GID 1'), (2, 'Alang-alang GID 2')]

def get_varieties():
    varieties = Variety.query.all()
    return ((i.var_name, i.var_name) for i in varieties)

@bp.route('/aap', methods=['GET', 'POST'])
def list_aap():
    items = AAP.query.all()
    form = AAPFilterForm()
    if form.submit():
        filters = [dict(PERIODS_).get(form.period.data),
            dict(get_varieties()).get(form.item.data),
            dict(WAREHOUSES_).get(form.warehouse.data)
            ]
    form.period.choices = PERIODS_
    form.item.choices = get_varieties()
    form.warehouse.choices = WAREHOUSES_
    return render_template('pages/listAAP.html', items=items, form=form,
        filters=filters)
