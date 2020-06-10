from flask import Blueprint, redirect, url_for, flash, request, jsonify, render_template
from flask_login import current_user, login_required
from app.models.Token import Token
from app.forms.TokenForm import TokenForm


bp = Blueprint('token', __name__)


@bp.route('/', methods=['GET'])
@login_required
def view():
    form = TokenForm()
    tokens = Token().all()
    return render_template('tokens.html', title='Tokens', tokens=tokens, form=form)


@bp.route('/generate', methods=['POST'])
@login_required
def generate():
    form = TokenForm(request.form)
    if form.validate_on_submit():
        api_key = Token.generate_api_key()
        token = Token.create(name=form.data.name, api_key=api_key)
        return jsonify(api_key=api_key)

