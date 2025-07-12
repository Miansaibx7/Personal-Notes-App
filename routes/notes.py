from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models.database import db, Note, User
from formwtf import NoteForm

notes = Blueprint('notes', __name__)

@notes.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for("auth.login"))
    
    form = NoteForm()
    user = User.query.get(session['user_id'])

    if form.validate_on_submit():
        note = Note(content=form.content.data, author=user)
        db.session.add(note)
        db.session.commit()
        flash("Note added successfully", "success")
        return redirect(url_for("notes.dashboard"))
    
    return render_template("dashboard.html", user=user, notes=user.notes, form=form)

@notes.route('/delete_note/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != session.get('user_id'):
        flash("Unauthorized", "danger")
        return redirect(url_for("notes.dashboard"))
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted", "info")
    return redirect(url_for("notes.dashboard"))

@notes.route('/edit_note/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != session.get('user_id'):
        flash("Unsauthorized", "danger")
        return redirect(url_for("notes.dashboard"))
    
    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.content = form.content.data
        db.session.commit()
        flash("Note updated successfully", "success")
        return redirect(url_for("notes.dashboard"))

    return render_template("edit_note.html", form=form, note=note)


