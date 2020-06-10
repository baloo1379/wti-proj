from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TokenForm(FlaskForm):
    name = StringField('Token name', validators=[DataRequired()])
    submit = SubmitField('Generate')
