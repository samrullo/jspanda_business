"""Routes for user authentication."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from .auth_forms import LoginForm, SignupForm
from .auth_model import db, User
from application import login_manager
import logging

_logger = logging.getLogger(__name__)
logging.basicConfig()
_logger.setLevel(logging.INFO)

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """User login page."""
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    login_form = LoginForm()
    # POST: Create user and redirect them to the app
    if login_form.validate_on_submit():
        _logger.info(f"will start login validation")
        # Get Form Fields
        login = login_form.login.data
        password = login_form.password.data
        # Validate Login Attempt
        _logger.info(f"Will look for the user {login}")
        user = User.query.filter_by(login=login).first()
        if user:
            _logger.info(f"Found user with {login} next will check password")
            if user.check_password(password=password):
                _logger.info(f"User {login} was authorized")
                login_user(user, remember=True)
                next = request.args.get('next')
                return redirect(next or url_for('main_bp.home'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login_page'))
    # GET: Serve Log-in page
    _logger.info("Probably first call. Will return login template")
    return render_template('login.html', form=login_form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """User sign-up page."""
    signup_form = SignupForm()
    # POST: Sign user in
    if signup_form.validate_on_submit():
        # Get Form Fields
        name = signup_form.name.data
        login = signup_form.login.data
        email = signup_form.email.data
        password = signup_form.password.data
        website = signup_form.website.data
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            logging.info("Will set up new user")
            user = User(name=name,
                        login=login,
                        email=email,
                        password=generate_password_hash(password, method='sha256'),
                        website=website)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main_bp.home'))
        flash('A user already exists with that email address.')
        return redirect(url_for('auth_bp.signup_page'))
    # GET: Serve Sign-up page
    return render_template('signup.html',
                           title='Create an Account | Flask-Login Tutorial.',
                           form=signup_form,
                           template='signup-page',
                           body="Sign up for a user account.")


@auth_bp.route("/logout")
@login_required
def logout_page():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login_page'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.', "danger")
    next = url_for(request.endpoint, **request.view_args)
    return redirect(url_for('auth_bp.login_page', next=next))
