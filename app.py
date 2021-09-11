from digicert import app, db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from digicert.models import User
from digicert.forms import LoginForm, RegistrationForm, ForgotPassword


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
            next_page = request.args.get('next')
            if next_page is None or not next_page[0] == '/':
                next_page = url_for('index')

            return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = str(form.email.data).split('@')[0]
        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=username,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('index'))


@app.route('/forgot_password')
def forgot_password():
    form = ForgotPassword()
    if form.validate_on_submit():
        if form.check_email(form.email):
            email = form.email.data
            print(email)
            redirect(url_for('index'))

    return render_template('forgot-password.html', form=form)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# All events
@app.route('/events/<event_type>')
def events(event_type):
    return render_template('events.html', type=event_type.capitalize())


@login_required
@app.route('/certificates')
def certificates():
    return render_template('certificates.html')


if __name__ == '__main__':
    app.run()
