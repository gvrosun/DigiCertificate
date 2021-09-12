from digicert import app, db
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, url_for, flash, Response
from flask_login import login_user, login_required, logout_user, current_user
from digicert.models import User, Certificate, Event
from datetime import date, timedelta
from digicert.forms import LoginForm, RegistrationForm, ForgotPasswordForm, \
    ContactUsForm, SubscribeForm, AddEventForm, \
    AddCertificateForm, SearchForm


@app.route('/', methods=['GET', 'POST'])
def index():
    contact_form = ContactUsForm()
    subscribe_form = SubscribeForm()
    if contact_form.validate_on_submit():
        pass
    if subscribe_form.validate_on_submit():
        pass
    return render_template('index.html', contact_form=contact_form, subscribe_form=subscribe_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
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


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        if form.check_email(form.email):
            email = form.email.data
            print(email)
            redirect(url_for('index'))

    return render_template('forgot-password.html', form=form)


@app.errorhandler(404)
def not_found(e):
    print(e)
    return render_template("404.html"), 404


# All events
@app.route('/events/<event_type>')
def events(event_type):
    total_events = Event.query.count()
    live_events = Event.query.filter(Event.end_date >= date.today(), Event.start_date < date.today()).all()
    upcoming_events = Event.query.filter(Event.start_date > date.today()).all()
    ended_events = Event.query.filter(Event.end_date < date.today()).all()
    if event_type == 'live':
        all_events = live_events
    elif event_type == 'upcoming':
        all_events = upcoming_events
    elif event_type == 'ended':
        all_events = ended_events
    else:
        return 'Bad Request', 404

    return render_template('events.html',
                           type=event_type.capitalize(),
                           events=all_events,
                           total_events=total_events,
                           total_live=len(live_events),
                           total_upcoming=len(upcoming_events),
                           total_ended=len(ended_events)
                           )


@login_required
@app.route('/certificates/<string:cert_type>')
def certificates(cert_type):
    uploaded = Certificate.query.filter_by(user_id=current_user.id, cert_type=cert_type).all()
    official = Certificate.query.filter_by(user_id=current_user.id, cert_type=cert_type).all()
    all_cert = Certificate.query.filter_by(user_id=current_user.id).all()
    if cert_type == 'uploaded':
        all_certificates = uploaded
    elif cert_type == 'official':
        all_certificates = official
    else:
        return 'Bad Request', 404

    total_cert = Certificate.query.count()
    total_uploaded = len(uploaded)
    total_official = len(official)
    this_year = date.today().year
    total_this_year = 0
    for cert in all_cert:
        if cert.obtained_date.year == this_year:
            total_this_year += 1
    return render_template('certificates.html',
                           certificates=all_certificates,
                           cert_type=cert_type.capitalize(),
                           total_cert=total_cert,
                           total_uploaded=total_uploaded,
                           total_official=total_official,
                           total_this_year=total_this_year,
                           this_year=this_year
                           )


@login_required
@app.route('/add_certificate', methods=['GET', 'POST'])
def add_certificate():
    form = AddCertificateForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        obtained_date = form.obtained_date.data
        cert_image = form.certificate_image.data

        filename = secure_filename(cert_image.filename)
        mimetype = cert_image.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        new_cert = Certificate(title=title,
                               description=description,
                               obtained_date=obtained_date,
                               cert_img=cert_image.read(),
                               cert_img_mimetype=mimetype,
                               cert_type='uploaded',
                               user_id=current_user.id
                               )
        db.session.add(new_cert)
        db.session.commit()
        flash('Certificate Uploaded')
        return redirect(url_for('index'))

    return render_template('add_certificate.html',
                           form=form,
                           today_date=date.today(),
                           start_date=date.today() - timedelta(days=36500)
                           )


@login_required
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    form = AddEventForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        logo = form.logo.data
        mode = form.mode.data

        filename = secure_filename(logo.filename)
        mimetype = logo.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        new_cert = Event(title=title,
                         description=description,
                         start_date=start_date,
                         end_date=end_date,
                         logo=logo.read(),
                         logo_mimetype=mimetype,
                         mode=mode
                         )
        db.session.add(new_cert)
        db.session.commit()
        flash('Event Added')
        return redirect(url_for('index'))

    return render_template('add_event.html',
                           form=form,
                           today_date=date.today(),
                           max_date=date.today() + timedelta(days=365)
                           )


@app.route('/certificates/preview/<string:slug>')
def view_certificate(slug):
    cert = Certificate.query.filter_by(slug=slug, user_id=current_user.id).first()
    if not cert:
        return 'Img Not Found!', 404

    return Response(cert.cert_img, mimetype=cert.cert_img_mimetype)


if __name__ == '__main__':
    app.run()
