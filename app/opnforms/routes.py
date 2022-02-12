from app.opnforms import bp
from flask import render_template

from app import db
from app.models import AAP

from flask_table import Table, Col

@bp.route('/aap', methods=['GET'])
def list_aap():
    items = AAP.query.all()
    table = AAPTable(items)
    return render_template('pages/listAAP.html', items=items, table=table)

class AAPTable(Table):
    classes = ['table', 'table-condensed', 'table-striped', 'responsive']
    doc_date = Col('Date')
    number = Col('Number')
    customer =Col('Customer')
