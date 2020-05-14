from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title= StringField('Title',validators=[DataRequired()])
    content= TextAreaField('Write Post', validators=[DataRequired()])
    submit=SubmitField('Post')

