from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField, SubmitField, DateField)     # form fields import
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired      # validators import



# Form to create new post
class PostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])

    content = TextAreaField(label='Content',widget=TextArea(), validators=[DataRequired()])

    submit = SubmitField(label='Post')


class SearchByDateForm(FlaskForm):
	from_ = DateField(label='From',default=date.today() - timedelta(30), format='%Y-%m-%d', validators=[DataRequired()])
	to_ = DateField(label='To', default=date.today, format='%Y-%m-%d', validators=[DataRequired()])
	submit = SubmitField(label='Search')



	

