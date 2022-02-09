from app.main import bp
from flask import render_template


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@bp.route('/aap', methods=['GET'])
def list_aap():
	return render_template('pages/listAAP.html')
