from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('標題', validators=[DataRequired(), Length(min=2, max=200)])
    subtitle = StringField('副標題', validators=[DataRequired(), Length(min=2, max=500)])
    content = TextAreaField('內容', validators=[DataRequired(), Length(min=10, max=5000)])
    submit = SubmitField('Post')