# coding=utf-8
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
import flask
from . import main
from .forms import EditProfileForm,PostFrom
from .. import db
from ..models import Permission, Role, User, Post, Comment



@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',active=1)


@main.route('/main', methods=['GET', 'POST'])
def main_page():
    form = PostFrom()
    if flask.request.method == 'GET':
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        return render_template('main.html',form=form,posts=posts)
    else:
        if current_user.can(Permission.WRITE) and form.validate():
            post = Post(body=form.body.data,author=current_user._get_current_object())
            db.session.add(post)
            return redirect(url_for('.main_page'))
        else:
            flash(u'您不具有发表的权限')
         #   Role.insert_roles()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('main.html', form=form, posts=posts)

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    #page = request.args.get('page', 1, type=int)
    #pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
    #    page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
    #    error_out=False)
    #posts = pagination.items
    # return render_template('user.html', user=user, posts=posts,
    #                      pagination=pagination)
    return render_template('user.html',user = user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if flask.request.method == "GET":
        return render_template('edit_profile.html', form=form,user=current_user)
    else:
        if form.validate():
            current_user.name = form.name.data
            current_user.location = form.location.data
            current_user.about_me = form.about_me.data
            db.session.add(current_user._get_current_object())
            db.session.commit()
            flash(u'个人信息已经更新')
          #  print current_user.location
            return redirect(url_for('.user', username=current_user.username))
        form.name.data = current_user.name
        form.location.data = current_user.location
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form,user=current_user)


