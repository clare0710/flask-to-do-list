from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .models.Item import Item
from .models.base import db

import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        item = request.form.get('items')
        date_string = request.form.get('datetime')
        if len(item) < 1:
            flash('Please enter a description!', category='error')
        elif date_string == "":
            flash('Please select a date!', category='error')
        else:
            date = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
            new_item = Item(description=item,
                            user_id=current_user.id, date=date)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added', category='success')

    items = Item.query.filter_by(
        user_id=current_user.id).order_by(Item.date.asc()).all()
    return render_template('home.html', user=current_user, items=items)


@views.route('/update-item', methods=['PATCH'])
@login_required
def update_item():
    item = json.loads(request.data)
    itemId = item['itemId']
    newDescription = item['description']
    newDate = item['date']
    item = db.session.get(Item, itemId)
    if item:
        if item.user_id == current_user.id:
            item.description = newDescription
            item.date = newDate
            item.is_expired = False
            db.session.commit()
            flash('Item updated', category='success')
            return jsonify({"message": "Item updated", "description": newDescription, "date": newDate, "is_expired": False})


@views.route('/delete-item', methods=['DELETE'])
@login_required
def delete_item():
    item = json.loads(request.data)
    itemId = item['itemId']
    item = db.session.get(Item, itemId)
    if item:
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            flash('Item deleted', category='success')
            return jsonify({"message": "Item deleted", "id": itemId})
