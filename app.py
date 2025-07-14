import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, TelField, SelectField, validators
from wtforms.validators import DataRequired, Email, Length, Regexp

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Google Sheets configuration
def get_google_sheet(sheet_name):
    try:
        import json
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        
        # Use hardcoded credentials for the service account
        creds_dict = {
            'type': 'service_account',
            'project_id': 'mealsfly-465908',
            'private_key_id': 'b0be13162b1cc30b21ea6afc7e6e48ab19b5272b',
            'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC0GQ/Z798niSo0\njtJBjog4uznLCA0ATRld3ROr4APcCIlkXOZIOzU8vtj35gMhZlqhSccZG0oB3Sxq\nGCA/he1fs1xP2Aj8lRCRcx/gwCaY3Py1PEwNXItCwg5QjE9balkbuEKhIxSEwFee\nyYPB9DEcOdND8a0J9e9uhU8QDUQz89H2Did+d5yDloufNFplRTiwTxCGPYsG14xw\nSwrvQ0neJX85yuW7l4qGHBTkfQf0aS00EUF48mca1veWaAF8rq5+ofrGmnawrU4y\n/QSntv/GrVRJXbfA9kjRss4Mu8hCoOkV5cLYqR46WdIfASw3p8/qdqB1Iq3/E1Cw\nqNXQBRGXAgMBAAECggEAJdteyaDyd40Noh6jc8RSPhqc+2Cl2vpZ6rEeAXMFXKsu\ntjoQ7f4EItC7KuDep5asVlr7zvs9g0bKn0KTBMdSLlu1e9MdkHqFEQ3yFXxOoLNT\nK4WRNv3NCCtiduwHgl/Ie1swJk8JcR49TNNvLsX1zMka751NklpwCftbszQWshSi\n88CgNuyVuTZJkqrtfMgUR14echApwN0ESLLVU0VpAFn7l/JjiQxDK5M8BR3PXKXl\nyiGu+g5xfVduv0ZlqdErU1ISR9QGGFK51es3DImrRRzPvT5JBwd1m98c3DrBp076\ncU+wvvD7ZjIwmlxwTfrUqaVzVzFi0gEFL5a3sPYZAQKBgQD93aJ9OoiZN++nq0+7\nE+wuNmdqm4OFQjFBXoQFpAyV8kFi1vUts5MVq8GUp2VAbMvGHSB0TJaiNlZbNT2+\n+vhm8elGrrwf91NRJ+ZCVk0GMOJAXa0SJK1mX8fcV86tIE1ztcdpeS6ZD2HeInoy\nwt/7Seix/EObWhK4Sjlv4hi12QKBgQC1nKpT5lWnUC+cIUz7WK12arJReOAoiVr5\nMqYNzYqeaB52cNjGr2rOzEKS0K69OeoRdVovEtYN0QKdvdYGJR2ngOBxAqQZ1uuj\nrx7X4QKoI8QmKw7ImLUstxuLNwO+CCY7ZBfFCAgnYDw2WtXdnGprlkHfEsy/7JZQ\nu4wakAIs7wKBgQCw6Y495Neipud9GhZDEdwqTEF/eoaKDBnVKy+n2q3mpN9KKPDN\ne3IJzRrnJEycO/U5x7yBL4pd2q4Ne6ne+Hi5DOZ7GnQBdtL6IGsHWartoI1bO6zL\nkwG/8QmPlSVzYqp283vXFdsSUTTrn203CLUcImJl/p2Cmp+nDBrAzHhZ6QKBgQCf\nunJz6BldVkEJaKB0T8IAbEb5MP61qFjC47D4YtaQC7L/KLD/zjh6OVw0FCYbd1xO\njpAK5t4suK88XUJnlS1HrSm5O0FpGIWXKOZPqC7WAt75UtVlyClQcptfDbvU3wYB\nJj9ho3bIavOKOsnuZyuSBE1bDQXXpxVtXAYVNqMzMQKBgQDeK8mGasGFa28d7+QE\ntAz0vaRfW7IRRseVu66tAsbrabZba3b6CaDo7n/1aKrSPFgOdl8fYKTNVfZVfdP0\nxaDB6DjK3qM82Yu6sVh5r/FvpCkyMpPVaXQuw5ni5DS7xhIrb9g9+eDtk8RJfRmD\nAiZ5okImf4DJuDJpeEBgDKLZMg==\n-----END PRIVATE KEY-----\n',
            'client_email': 'mealsfly@mealsfly-465908.iam.gserviceaccount.com',
            'client_id': '104052847552527103619',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/mealsfly%40mealsfly-465908.iam.gserviceaccount.com',
            'universe_domain': 'googleapis.com'
        }
        print("Using hardcoded service account credentials")
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        print(f"Attempting to open sheet by URL, worksheet: {sheet_name}")
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1IhOhF0Umd4_qps_yQocrAj6CzFHvxiRE47QGUJiLUJ0/edit?usp=sharing").worksheet(sheet_name)
        print(f"Successfully opened worksheet: {sheet_name}")
        
        # Check if headers exist, if not add them
        setup_sheet_headers(sheet, sheet_name)
        
        return sheet
    except Exception as e:
        print(f"Error accessing Google Sheets: {e}")
        return None

def setup_sheet_headers(sheet, sheet_name):
    try:
        # Check if first row has headers
        first_row = sheet.row_values(1)
        
        if sheet_name == "Partners":
            headers = ["Restaurant Name", "Owner Name", "Email", "Phone", "Address", "Cuisine Type", "Experience", "Description"]
        elif sheet_name == "Riders":
            headers = ["Full Name", "Email", "Phone", "Address", "Vehicle Type", "License Number", "Experience", "Availability"]
        else:
            return
            
        # If no headers or wrong headers, set them
        if not first_row or first_row != headers:
            sheet.insert_row(headers, 1)
            print(f"Headers added to {sheet_name} sheet")
            
    except Exception as e:
        print(f"Error setting up headers: {e}")

# Partner Form
class PartnerForm(FlaskForm):
    restaurant_name = StringField('Restaurant Name', validators=[DataRequired(), Length(min=2, max=100)])
    owner_name = StringField('Owner Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[
        DataRequired(), 
        Regexp(r'^[0-9]{10}$', message="Phone number must be exactly 10 digits")
    ])
    address = TextAreaField('Restaurant Address', validators=[DataRequired(), Length(min=10, max=200)])
    cuisine_type = SelectField('Cuisine Type', choices=[
        ('indian', 'Indian'),
        ('chinese', 'Chinese'),
        ('italian', 'Italian'),
        ('mexican', 'Mexican'),
        ('fast_food', 'Fast Food'),
        ('south_indian', 'South Indian'),
        ('north_indian', 'North Indian'),
        ('continental', 'Continental'),
        ('desserts', 'Desserts'),
        ('beverages', 'Beverages'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    experience = SelectField('Restaurant Experience', choices=[
        ('new', 'New Restaurant'),
        ('1-2', '1-2 Years'),
        ('3-5', '3-5 Years'),
        ('5+', '5+ Years')
    ], validators=[DataRequired()])
    description = TextAreaField('Restaurant Description', validators=[Length(max=500)])

# Rider Form  
class RiderForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[
        DataRequired(), 
        Regexp(r'^[0-9]{10}$', message="Phone number must be exactly 10 digits")
    ])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    vehicle_type = SelectField('Vehicle Type', choices=[
        ('bike', 'Motorcycle/Bike'),
        ('scooter', 'Scooter'),
        ('bicycle', 'Bicycle'),
        ('car', 'Car')
    ], validators=[DataRequired()])
    license_number = StringField('Driving License Number', validators=[DataRequired(), Length(min=5, max=20)])
    experience = SelectField('Delivery Experience', choices=[
        ('fresher', 'No Experience (Fresher)'),
        ('1-2', '1-2 Years'),
        ('3-5', '3-5 Years'),
        ('5+', '5+ Years')
    ], validators=[DataRequired()])
    availability = SelectField('Availability', choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('weekends', 'Weekends Only')
    ], validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/become-partner', methods=['GET', 'POST'])
def become_partner():
    form = PartnerForm()
    if form.validate_on_submit():
        try:
            # Try Google Sheets first
            sheet = get_google_sheet("Partners")
            if sheet:
                sheet.append_row([
                    form.restaurant_name.data,
                    form.owner_name.data,
                    form.email.data,
                    form.phone.data,
                    form.address.data,
                    form.cuisine_type.data,
                    form.experience.data,
                    form.description.data
                ])
                flash('Thank you! Your partner application has been submitted successfully.', 'success')
                return redirect(url_for('become_partner'))
            else:
                # Fallback: Log to console for now
                print("=== PARTNER APPLICATION SUBMITTED ===")
                print(f"Restaurant: {form.restaurant_name.data}")
                print(f"Owner: {form.owner_name.data}")
                print(f"Email: {form.email.data}")
                print(f"Phone: {form.phone.data}")
                print(f"Address: {form.address.data}")
                print(f"Cuisine: {form.cuisine_type.data}")
                print(f"Experience: {form.experience.data}")
                print(f"Description: {form.description.data}")
                print("=====================================")
                flash('Thank you! Your partner application has been received. (Note: Google Sheets integration needs to be configured)', 'success')
                return redirect(url_for('become_partner'))
        except Exception as e:
            print(f"Error: {e}")
            # Fallback: Log to console
            print("=== PARTNER APPLICATION (FALLBACK) ===")
            print(f"Restaurant: {form.restaurant_name.data}")
            print(f"Owner: {form.owner_name.data}")
            print(f"Email: {form.email.data}")
            print(f"Phone: {form.phone.data}")
            print(f"Address: {form.address.data}")
            print(f"Cuisine: {form.cuisine_type.data}")
            print(f"Experience: {form.experience.data}")
            print(f"Description: {form.description.data}")
            print("====================================")
            flash('Thank you! Your partner application has been received. (Note: Google Sheets integration needs to be configured)', 'success')
            return redirect(url_for('become_partner'))
    
    return render_template('partner_form.html', form=form)

@app.route('/become-rider', methods=['GET', 'POST'])
def become_rider():
    form = RiderForm()
    if form.validate_on_submit():
        try:
            # Try Google Sheets first
            sheet = get_google_sheet("Riders")
            if sheet:
                sheet.append_row([
                    form.full_name.data,
                    form.email.data,
                    form.phone.data,
                    form.address.data,
                    form.vehicle_type.data,
                    form.license_number.data,
                    form.experience.data,
                    form.availability.data
                ])
                flash('Thank you! Your rider application has been submitted successfully.', 'success')
                return redirect(url_for('become_rider'))
            else:
                # Fallback: Log to console for now
                print("=== RIDER APPLICATION SUBMITTED ===")
                print(f"Name: {form.full_name.data}")
                print(f"Email: {form.email.data}")
                print(f"Phone: {form.phone.data}")
                print(f"Address: {form.address.data}")
                print(f"Vehicle: {form.vehicle_type.data}")
                print(f"License: {form.license_number.data}")
                print(f"Experience: {form.experience.data}")
                print(f"Availability: {form.availability.data}")
                print("===================================")
                flash('Thank you! Your rider application has been received. (Note: Google Sheets integration needs to be configured)', 'success')
                return redirect(url_for('become_rider'))
        except Exception as e:
            print(f"Error: {e}")
            # Fallback: Log to console
            print("=== RIDER APPLICATION (FALLBACK) ===")
            print(f"Name: {form.full_name.data}")
            print(f"Email: {form.email.data}")
            print(f"Phone: {form.phone.data}")
            print(f"Address: {form.address.data}")
            print(f"Vehicle: {form.vehicle_type.data}")
            print(f"License: {form.license_number.data}")
            print(f"Experience: {form.experience.data}")
            print(f"Availability: {form.availability.data}")
            print("==================================")
            flash('Thank you! Your rider application has been received. (Note: Google Sheets integration needs to be configured)', 'success')
            return redirect(url_for('become_rider'))
    
    return render_template('rider_form.html', form=form)

@app.route('/download')
def download():
    # Placeholder for download analytics tracking
    return render_template('index.html')
