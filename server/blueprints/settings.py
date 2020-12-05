from flask import json, request, Blueprint, render_template, session, redirect, url_for
from server.db import db
from server.models.Admin import Admin

settings = Blueprint('settings', __name__, template_folder='templates')


@settings.route('/admin/settings', methods=["GET"])
def show_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    current_user = Admin.query.filter_by(username=session['username']).first()

    return render_template('settings.html', user=session['username'], title='Settings', current_user=current_user)


@settings.route('/admin/settings', methods=["POST"])
def change_settings():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    current_user = Admin.query.filter_by(username=session['username']).first()

    updates = request.get_json()

    current_user.first_name = updates["first_name"] if updates["first_name"] != '' else current_user.first_name
    current_user.last_name = updates["last_name"] if updates['last_name'] != '' else current_user.last_name
    current_user.username = updates["username"] if updates['username'] != '' else current_user.username
    current_user.password = updates["password"] if updates['password'] != '' else current_user.password
    current_user.role = updates["role"] if updates['role'] != '' else current_user.role

    db.session.add(current_user)
    db.session.commit()

    session['username'] = current_user.username

    updated_user = {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "username": current_user.username,
        "password": current_user.password,
        "role": current_user.role,
    }

    return json.dumps(updated_user)
