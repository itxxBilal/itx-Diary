from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import DiaryEntry
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    entries = DiaryEntry.query.order_by(DiaryEntry.timestamp.desc()).all()
    return render_template('index.html', entries=entries)

@bp.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_entry = DiaryEntry(title=title, content=content)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('entry.html')

@bp.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    if request.method == 'POST':
        entry.title = request.form['title']
        entry.content = request.form['content']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit_entry.html', entry=entry)

@bp.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('main.index'))
