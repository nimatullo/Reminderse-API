from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Optional


class AddLink(FlaskForm):
    entry_title = StringField('Entry Title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    category = StringField('Category (Optional)')
    submit_1 = SubmitField('Add To Entries')


class EditLink(FlaskForm):
    entry_title = StringField('Entry Title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    date_of_next_send = IntegerField(label='Days Until Next Send', validators=[Optional()])
    category = StringField('Category (Optional)')
    submit = SubmitField('Save Link Changes')


class EditText(FlaskForm):
    entry_title = StringField('Entry Title', validators=[DataRequired()])
    text_content = TextAreaField('Text Content', validators=[DataRequired()])
    date_of_next_send = IntegerField(label='Days Until Next Send', validators=[Optional()])
    category = StringField('Category (Optional)')
    submit_text = SubmitField('Save Text Changes')


class AddText(FlaskForm):
    entry_title = StringField('Entry Title', validators=[DataRequired()])
    text_content = TextAreaField('Text Content', validators=[DataRequired()])
    category = StringField('Category (Optional)')
    submit_2 = SubmitField('Add To Entries')


class Search(FlaskForm):
    query = StringField('Entry Title', validators=[DataRequired()])
    submit = SubmitField('Search')
