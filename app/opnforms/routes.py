from app.opnforms import bp
from flask import render_template, request

from .forms import AAPFilterForm
from app import db
from app.models import Variety, Warehouse, Branch, AAP
from datetime import date


# from flask_table import Table, Col
PERIODS_ = [('today', 'Today'), ('yesterday', 'Yesterday'),\
    ('thisweek', 'This week'), ('lastweek', 'Last week'),\
    ('thisquarter', 'This quarter'), ('lastquarter', 'Last quarter'),\
    ('thisyear', 'This Year'), ('lastyear', 'Last year')] 

BRANCH = Branch.query.filter(Branch.branch_name == 'Leyte Branch').first()

def get_period(token):
    if token == 'today':
        period = date.today()
    else:
        period = date.today()
    return period

def get_varieties():
    varieties = Variety.query.all()
    var = tuple(((i.var_name, i.var_name) for i in varieties))
    return (('any', '- Any Variety -'),) + var

def get_warehouses():
    whses = Warehouse.query.filter(Warehouse.branch_id == BRANCH.id).all()
    tup = tuple(((i.id, i.warehouse_name) for i in whses))
    if len(tup) > 1:
        tup = ((-1, '- Any Warehouse -'),) + tup
    return tup

@bp.route('/aap', methods=['GET', 'POST'])
def list_aap():
    # items = AAP.query.all()
    form = AAPFilterForm()
    form.period.choices = PERIODS_
    form.item.choices = get_varieties()
    form.warehouse.choices = get_warehouses()
    if form.submit():
        if request.form.get('period'):
            filters = [dict(PERIODS_).get(form.period.data),
                dict(get_varieties()).get(form.item.data),
                dict(get_warehouses()).get(form.warehouse.data)
                ]
            # filter_values = [Date()]
        else:
            filters = [PERIODS_[0][1], form.item.choices[0][1], form.warehouse.choices[0][1]]
    items = AAP.query.filter_by(
        doc_date = get_period(filters[0]))
    return render_template('pages/listAAP.html', items=items, form=form,
        filters=filters)
