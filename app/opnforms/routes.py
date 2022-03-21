from app.opnforms import bp
from flask import render_template, request, url_for

from .forms import AAPFilterForm, AAPForm
from app import db
from app.models import Variety, Warehouse, Branch, AAP, Item
from datetime import datetime, date
import calendar

DFMT = '%m/%d/%Y'
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
    return tup

def get_items():
    return Item.query

def get_warehouses_fac():
    return Warehouse.query.filter(Warehouse.branch_id == BRANCH.id)

@bp.route('/aap', methods=['GET', 'POST'])
def list_aap():
    WAREHOUSES_ = get_warehouses()
    VARIETIES_ = get_varieties()
    period_range = [date.today(), date.today()]
    form = AAPFilterForm()
    form.item.choices = VARIETIES_
    form.warehouse.choices = WAREHOUSES_
    if request.method == 'GET':
        form.date1.data = period_range[0]
        form.date2.data = period_range[1]
        filters = [period_range, form.item.choices[0][1], form.warehouse.choices[0][1]]

    if form.submit():
        if 'submit' in request.form:
            filters = [[form.date1.data, form.date2.data],
                dict(VARIETIES_).get(form.item.data),
                dict(WAREHOUSES_).get(form.warehouse.data)
                ]
    period_range = filters[0]
    items = AAP.query.filter(
        AAP.doc_date.between(period_range[0], period_range[1]),
        )
    return render_template('pages/listAAP.html', items=items, form=form,
        filters=filters)

@bp.route('/aap-new', methods=['GET', 'POST'])
def aap_new():
    form = AAPForm()

    if request.method == 'GET':
        form.item_id.query_factory = get_items
        form.warehouse_id.query_factory = get_warehouses_fac
        items = tuple( (i.id, str(round(i.selling_price,2)), i.variety.commodity.is_cereal) for i in get_items() )
    return render_template('pages/AAPAdd.html', form=form, items=items)

@bp.route('/test-page', methods=['GET', 'POST'])
def test_page():
    form = AAPForm()

    if request.method == 'GET':
        form.item_id.query_factory = get_items
        form.warehouse_id.query_factory = get_warehouses_fac
        items = tuple( (i.id, str(round(i.selling_price,2)), i.variety.commodity.is_cereal) for i in get_items() )
        return render_template('pages/test-page.html', form=form, items=items)
