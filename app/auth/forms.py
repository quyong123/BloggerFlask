# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo,Email
from ..models import User
from .. import db
from wtforms import ValidationError
class LoginForm(FlaskForm):
    """
    用户登陆表单
    """
    email = StringField('your email?',validators = [DataRequired(),Email(message=u'邮箱格式错误')])
    password = PasswordField('password',validators=[Length(1,64,message=u'密码须在1-64位')])
    submit = SubmitField(u'登陆')


class RegistrationForm(FlaskForm):
    """
    用户注册的表单
    """
    email = StringField(u'邮箱：',validators=[Email(message=u'邮箱格式错误')])
    username = StringField(u'用户名：',validators=[Length(1,64,message=u'用户名长度1-64'),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,message=u'需是字母')])
    password1 = PasswordField(u'密码：',validators=[Length(1,64,message=u'密码须在1-64位'),EqualTo('password2',message=u'两次输入的密码不一致')])
    password2 = PasswordField(u'确认密码：',validators=[Length(1,64,message=u'密码须在1-64位')])
    submit = SubmitField(u'提交')

    def validate_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError(u'邮箱早已被注册')

    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError(u'用户名早已存在')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('New Email', validators=[Email(message=u'邮箱格式错误')])
    submit = SubmitField(u'提交')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2',message=u'两次输入的密码不一致')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码',validators=[Length(1,64,message=u'密码须在1-64位'),])
    password1 = PasswordField(u'新密码',validators=[Length(1,64,message=u'密码须在1-64位'),EqualTo('password2',message=u'两次输入的密码不一致')])
    password2 = PasswordField(u'确认密码',validators=[Length(1,64,message=u'密码须在1-64位'),])
    submit = SubmitField(u'提交')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[Email(message=u'邮箱格式错误')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱早已被注册')