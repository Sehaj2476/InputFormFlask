# app.py
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TelField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Contact {self.first_name} {self.last_name}>'

# Form Class
class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    phone = TelField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+?1?\d{9,15}$', message="Please enter a valid phone number")
    ])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        db.session.add(contact)
        db.session.commit()
        flash('Your contact information has been saved!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/contacts')
def view_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('contacts.html', contacts=contacts)

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)