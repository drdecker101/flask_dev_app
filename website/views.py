from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

from .script import convertOMCtoOFX , convertOMCtoGE100L, convertLAGtoTSV, replicate

views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("omcToOfx.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/OMCtoOFX',methods=['GET','POST'])
def omcToOfx():
    cid_output = ""
    if request.method == 'POST':
        cid = request.form.get('cid')
        
        if len(cid.split(".")) != 4:
            flash(f'Check OMC path {cid} inputted.', category='error')
        else:
            cid_output = convertOMCtoOFX(cid) 
    return render_template("omcToOfx.html", user=current_user, cid = cid_output)

@views.route('/OMCtoGE100L',methods=['GET','POST'])
def omcToGE100L():
    cid_output = ""
    if request.method == 'POST':
        cid = request.form.get('cid')
        code = request.form.get('code')
        side = request.form.get('side')

        
        if len(cid.split(".")) != 4:
            flash(f'Check OMC path {cid} inputted.', category='error')

        else:
            cid_output = convertOMCtoGE100L(cid, code, side) 
    return render_template("omcTo100L.html", user=current_user, cid = cid_output)

@views.route('/LAGtoTSV',methods=['GET','POST'])
def lagToTsv():
    cids = [""]
    if request.method == 'POST':
        cid = request.form.get('cid')
        ces = request.form.get('ces')
        
        if len(cid.split(".")) != 4:
            flash(f'Check OMC path {cid} inputted.', category='error')
        elif ces == "Choose...":
            flash(f'Check CES inputted.', category='error')
        else:
            cids= convertLAGtoTSV(cid, ces) 
    return render_template("lagTotsv.html", user=current_user, cids = cids)

@views.route('/Notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

