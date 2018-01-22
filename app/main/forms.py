# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask.ext.pagedown.fields import PageDownField

class EditProfileForm(FlaskForm):
    name = StringField(u'姓名', validators=[Length(1, 64)])
    location = StringField(u'所在地', validators=[Length(1, 64)])
    tel = StringField(u'联系电话', validators=[Length(1, 64)])
    qq = StringField(u'QQ', validators=[Length(1, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'保存')


class PostFrom(FlaskForm):
    body = TextAreaField(u'你的想法',validators=[DataRequired()])
    submit = SubmitField(u'提交')


