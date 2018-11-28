from flask import request, url_for, redirect, render_template, abort, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, Role
from app.decorators import permission_required, admin_required
from app import db
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u is not None and u.verify_password(form.password.data):
            login_user(u, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data,
                 email=form.email.data,
                 password=form.password.data)
        db.session.add(u)
        db.commit()
        flash('you can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset_password', methods=['POST'])
def password_reset(id):
    pass


@admin_required
def all_users():
    users = User.query.all()
    render_template('auth/all_users.html', user=users)
