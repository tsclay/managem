import datetime
from functools import wraps
from flask.helpers import make_response
from flask import current_app, g

from flask.json import jsonify
from server.blueprints import decrypt
from datetime import timezone
from flask_wtf import csrf
from flask import Blueprint, url_for, render_template, request, session, redirect
import json
from server.db import db
from server.models.Admin import Admin
from server.limiter import limiter
from . import skip_redirect

auth = Blueprint('auth', __name__, template_folder='../templates')


@auth.before_request
def redirect_for_client(*args, **kw):
    if request.method != "GET":
        return
    view_func = current_app.view_functions[request.endpoint]
    current_app.logger.info(view_func)
    g.skip_redirect = hasattr(view_func, '_skip_redirect')
    current_app.logger.info(g.skip_redirect)
    if not g.skip_redirect:
        current_app.logger.info("redirecting this GET request!")
        response = make_response(redirect('/'))
        if current_app.config["ENV"] == "development":
            response = make_response(redirect('http://localhost:5173'))

        response.headers['X-Client-Redirect'] = '/login'
        return response


@auth.errorhandler(429)
def handle_excess_attempts(e):
    return make_response(jsonify(error="For security reasons, you are unable to make login attempts for one hour."), 429)


# @auth.route('', methods=["GET"])
# def home():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))

#     return render_template('home.html', user=session["username"], role=session["role"], title='Home')

@auth.route('/csrf-token', methods=["GET"])
@skip_redirect()
def get_csrf_token():
    return make_response(jsonify(token=csrf.generate_csrf()), 200)


@auth.route('/auth-check', methods=['POST'])
@skip_redirect()
def check_auth():
    data = request.get_json()
    current_app.logger.info(session)
    if 'username' not in session:
        return make_response(jsonify({}), 200)
    return make_response(jsonify({"username": session["username"], "role": session["role"], "first_name": session["first_name"], "last_name": session["last_name"]}), 200)


@auth.route('/login', methods=["GET", "POST"])
@limiter.limit('5/hour', override_defaults=True, deduct_when=lambda response: response.status_code == 401)
def login():
    current_app.logger.info(current_app.config)

    current_app.logger.info(request.url)
    # if request.method == "GET":
    #     message = request.args.get('message')
    #     if message is not None:
    #         return redirect('/')
    #         return render_template('login.html', message=json.loads(message))
    #     else:
    #         return render_template('login.html')

    data = request.get_json()
    username = data["username"]
    password = data["password"]
    found_user = Admin.query.filter_by(
        username=username).first()
    if found_user is not None and \
            username == found_user.username and \
            password == decrypt(found_user.password):
        session["username"] = found_user.username
        session["role"] = found_user.role
        session["first_name"] = found_user.first_name
        session["last_name"] = found_user.last_name
        current_app.logger.info(session)
        found_user.active = True
        found_user.last_logged_in = datetime.datetime.now(timezone.utc)
        db.session.add(found_user)
        db.session.commit()
        # return redirect(url_for('auth.home'), 302)
        return make_response(jsonify(message="Authenticated.", username=found_user.username, role=found_user.role), 200)
    else:
        return make_response(jsonify(error="Double-check your credentials and try again."), 401)


@auth.route('/logout', methods=["POST"])
def logout():
    # if 'username' not in session:
    #     return redirect(url_for('auth.login'))
    user_data = request.get_json()

    found_user = Admin.query.filter_by(
        username=user_data['username']).first()
    found_user.active = False
    db.session.add(found_user)
    db.session.commit()
    current_app.logger.info(session)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('first_name', None)
    session.pop('last_name', None)

    current_app.logger.info(session)

    return make_response(jsonify(message='Logout successful'), 200)
