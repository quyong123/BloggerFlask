# coding=utf-8
from flask import render_template, flash,redirect,url_for,request
from flask_login import login_user, logout_user, login_required, current_user
import flask
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,ChangeEmailForm,PasswordResetRequestForm,PasswordResetForm
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if flask.request.method == "GET":
        return render_template("auth/login.html", form=form)
    else:
        if form.validate() :
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user,False)
                return redirect(request.args.get('next') or url_for('main.index'))
            flash(u'不合法的用户名或密码')
            return render_template("auth/login.html", form=form,active=7)
        else:
            print form.errors
            return render_template("auth/login.html", form=form,active=7)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经被登出.')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if flask.request.method == "GET":
        return render_template('auth/register.html',form = form)
    else:
        if form.validate():
            user = User(email = form.email.data,username = form.username.data,password = form.password1.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(form.email.data, 'confirm','auth/email/confirm',user=user,token=token)
            flash(u'确认邮件已发送到你的账户')
            return redirect(url_for('auth.login'))
        else:
            print form.errors
            return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if flask.request.method == 'GET':
        return render_template("auth/change_password.html", form=form)
    else:
        if form.validate():
            if current_user.verify_password(form.old_password.data):
                current_user.password = form.password1.data
                db.session.add(current_user)
                db.session.commit()
                flash(u'您的密码已经被修改')
                return redirect(url_for('main.index'))
            else:
                flash(u'旧密码错误.')
                return render_template("auth/change_password.html", form=form)
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():

    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if flask.request.method == 'GET':
        return render_template("auth/reset_password.html", form=form)
    else:
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.generate_reset_token()
                send_email(user.email, 'Reset Your Password',
                           'auth/email/reset_password',
                           user=user, token=token,
                           next=request.args.get('next'))
            flash(u'重置密码的邮件已发送到邮箱')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if flask.request.method == 'GET':
        return render_template("auth/reset_passwordnew.html", form=form)
    else:
        if form.validate():
            if User.reset_password(token, form.password.data):
                db.session.commit()
                flash(u'您的密码已经被更新.')
                return redirect(url_for('auth.login'))
            else:
                return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if flask.request.method == 'GET':
        return render_template("auth/change_email.html", form=form)
    else:
        if form.validate():
            if current_user.verify_password(form.password.data):
                new_email = form.email.data
                token = current_user.generate_email_change_token(new_email)
                send_email(form.email.data, 'confirm', 'auth/email/change_email', user=current_user, token=token)
                flash(u'确认邮件已发送到你的账户')
                return redirect(url_for('main.index'))
            else:
                flash(u'邮箱不合法或者密码错误')
                return render_template("auth/change_email.html", form=form)
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash(u'你的邮箱地址已经被更新.')
    else:
        flash(u'不合法的请求.')
    return redirect(url_for('main.index'))
