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
        token = Token.create(name=form.data.get('name'), api_key=api_key)
        flash(f"Your \"{token.name}\" token's ID is {token.id}")
    return redirect(url_for('token.view'))


@bp.route('/<idx>', methods=['GET'])
@login_required
def get(idx):
    token = Token.find_one(idx)
    return jsonify(api_key=token.api_key_hash)


@bp.route('/<idx>', methods=['DELETE'])
@login_required
def delete(idx):
    token = Token.find_one(idx)
    token.delete()
    flash('Token deleted successfully')
    return jsonify(deleted=True)

