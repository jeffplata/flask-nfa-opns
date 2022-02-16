from app.opnforms import bp
from flask import render_template

from .forms import AAPFilterForm
from app import db
from app.models import Variety, Warehouse, Branch, AAP


# from flask_table import Table, Col
PERIODS_ = [('today', 'Today'), ('yesterday', 'Yesterday'),\
    ('thisweek', 'This week'), ('lastweek', 'Last week'),\
    ('thisquarter', 'This quarter'), ('lastquarter', 'Last quarter'),\
    ('thisyear', 'This Year'), ('lastyear', 'Last year')] 

ITEMS_ = [('WD1', 'WD1'), ('WD2', 'WD2'), ('PD1', 'PD1'), ('PD3', 'PD3')]

WAREHOUSES_ = [(1, 'Alang-alang GID 1'), (2, 'Alang-alang GID 2')]

BRANCH = Branch.query.filter(Branch.branch_name == 'Leyte Branch').first()

def get_varieties():
    varieties = Variety.query.all()
    var = tuple(((i.var_name, i.var_name) for i in varieties))
    return (('any', '- Any Variety -'),) + var

def get_warehouses():
    whses = Warehouse.query.filter(Warehouse.branch_id == BRANCH.id).all()
    tup = tuple(((i.id, i.warehouse_name) for i in whses))
    if len(tup) > 1:
        tup = ((-1, '- Any Warehouse -'),) + tup
    print(tup)
    return tup

@bp.route('/aap', methods=['GET', 'POST'])
def list_aap():
    items = AAP.query.all()
    form = AAPFilterForm()
    if form.submit():
        filters = [dict(PERIODS_).get(form.period.data),
            dict(get_varieties()).get(form.item.data),
            dict(get_warehouses()).get(form.warehouse.data)
            ]
    form.period.choices = PERIODS_
    form.item.choices = get_varieties()
    form.warehouse.choices = get_warehouses()
    return render_template('pages/listAAP.html', items=items, form=form,
        filters=filters)
