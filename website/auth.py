from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.omcToOfx'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # return redirect(url_for('views.home'))
            return redirect(url_for('views.omcToOfx'))

    return render_template("sign_up.html", user=current_user)  



# from .script import convertOMCtoOFX , convertOMCtoGE100L, replicate
# @auth.route('/signin',methods=['GET','POST'])
# def signin():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password1 = request.form.get('password1')

#         print(email)
#         print(password1)

#         if len(email) < 4 and email != "12345@gmail.com":
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(password1) < 4:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             flash('Account created.', category='success')

#     return render_template("signin.html")

# @auth.route('/OMCtoOFX',methods=['GET','POST'])
# def omcToOfx():
#     cid_output = ""
#     if request.method == 'POST':
#         cid = request.form.get('cid')
#         # code = request.form.get('code')
        
#         if len(cid.split(".")) != 4:
#             flash(f'Check OMC path {cid} inputted.', category='error')
#         else:
#             cid_output = convertOMCtoOFX(cid) 
#     return render_template("omcToOfx.html", cid = cid_output)

# @auth.route('/OMCtoGE100L',methods=['GET','POST'])
# def omcToGE100L():
#     cid_output = ""
#     if request.method == 'POST':
#         cid = request.form.get('cid')
#         code = request.form.get('code')
#         side = request.form.get('side')

        
#         if len(cid.split(".")) != 4:
#             flash(f'Check OMC path {cid} inputted.', category='error')
#         # elif code.upper() not in ["MCR","M","EDR","E"]:
#         #    flash(f'Check entity code {code} inputted.', category='error') 
#         else:
#             cid_output = convertOMCtoGE100L(cid, code, side) 
#     return render_template("omcTo100L.html", cid = cid_output)

# @auth.route('/checkID',methods=['GET','POST'])
# def checkId():
#     cid_output = ""
#     if request.method == 'POST':
#         cid = request.form.get('cid')
#         code = request.form.get('code')
        
#         if len(cid.split(".")) != 4:
#             flash(f'Check OMC path {cid} inputted.', category='error')
#         elif code.upper() not in ["OTE","OTF","OT1","OT2","OT3"]:
#            flash(f'Check entity code {code} inputted.', category='error') 
#         else:
#             cid_output = convertOMCtoOFX(cid, code) 
#     return render_template("login.html", cid = cid_output)


# @auth.route('/replicateLagID',methods=['GET','POST'])
# def replicateLagId():

    # lag_ids = [""]
    # if request.method == 'POST':
    #     inp1 = request.form.get('inp1')
    #     inp2 = request.form.get('inp2')
    #     range1 = request.form.get('range1')

    #     if "Choose..." not in [inp1, inp2, range1]:
    #         lag_ids = replicate(inp1, inp2, int(range1))
             
    # return render_template("replicate.html", lag_ids = lag_ids)
