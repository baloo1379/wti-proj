from flask import Blueprint, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required

from app.models.Job import Job
from app.models.Token import Token
from app.forms.NewPredictionForm import NewPredictionForm

bp = Blueprint('job', __name__)


@bp.route('/', methods=['POST'])
@login_required
def create():
    form = NewPredictionForm(request.form)
    if form.validate_on_submit():
        flash(form.data.data)
        Job.create(name='fruits', data=form.data.data, current_user=current_user)
    return redirect(url_for('index.dashboard'))


@bp.route('/<idx>', methods=['GET'])
@login_required
def read(idx):
    job = Job.find_one(by={'id': idx, 'user_id': current_user.id})
    if job is None:
        return jsonify(error='Not Found'), 404
    return jsonify(job=job.to_dict())


@bp.route('/queue', methods=['GET'])
def queue():
    if 'api_key' in request.args:
        api_key = request.args.get('api_key')
        token = Token.find_one(by={'api_key_hash': api_key})
        if token is not None:
            job = Job.pop()
            if job is None:
                return jsonify(error='Not Found'), 404
            job.set_status(Job.RUNNING)
            return jsonify(job.to_dict())
        else:
            return jsonify(error='Wrong API key'), 401
    else:
        return jsonify(error='No API key'), 401


@bp.route('/<idx>', methods=['POST'])
def update(idx):
    if 'api_key' in request.args:
        api_key = request.args.get('api_key')
        token = Token.find_one(by={'api_key_hash': api_key})
        if token is not None:
            job = Job.find_one(idx)
            if job is None:
                return jsonify(error='Not Found'), 404
            data = request.get_json()
            if 'status' in data:
                job.set_status(data.get('status'))
            if 'result' in data:
                job.set_result(data.get('result'))
            return jsonify(job.to_dict())
        else:
            return jsonify(error='Wrong API key'), 401
    else:
        return jsonify(error='No API key'), 401


@bp.route('/test', methods=['GET'])
def test():
    if 'api_key' in request.args:
        api_key = request.args.get('api_key')
        token = Token.find_one(by={'api_key_hash': api_key})
        if token is not None:
            return jsonify(ok=True)
        else:
            return jsonify(error='Wrong API key'), 401
    else:
        return jsonify(error='No API key'), 401
