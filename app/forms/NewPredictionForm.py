from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewPredictionForm(FlaskForm):
    data = TextAreaField('Raw JSON data', validators=[DataRequired()])
    submit = SubmitField('Add')
