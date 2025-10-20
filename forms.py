from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, RadioField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Optional

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = TextAreaField('Author', validators=[DataRequired()])
    genre = TextAreaField('Genre', validators=[DataRequired()])
    pages = IntegerField('Number of Pages', validators=[DataRequired(), NumberRange(min=1)])
    cover = RadioField('Choose a Cover Design', 
                      choices=[('img/book0.png', 'Cover 1'), ('img/book00.png', 'Cover 2')],
                      validators=[DataRequired()])
    status = HiddenField('Status', default='Reading Now')
    pages_read = IntegerField('Pages Read', validators=[Optional(), NumberRange(min=0)], default=0)
    notes = TextAreaField('Notes', validators=[Optional()])
    rating = HiddenField('Rating', validators=[Optional()])
    submit = SubmitField('Submit')

# Keep the old form for backward compatibility if needed
class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
