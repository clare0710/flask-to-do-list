from flask_mail import Message, Mail
from datetime import datetime
from .models.User import User
from .models.Item import Item
from .models.base import db


mail = Mail()


def send_email(app):
    with app.app_context():
        users = User.query.all()
        for user in users:
            new_expired_items = Item.query.filter_by(user_id=user.id).filter(
                Item.date < datetime.now()).order_by(Item.date.asc()).filter(Item.is_expired == False).all()

            if new_expired_items:
                print('expired!!!' + str(datetime.now()))
                msg = Message('Expired Items',
                              recipients=[user.email])
                msg.body = 'The following items have expired:\n'

                for item in new_expired_items:
                    item.is_expired = True
                    db.session.commit()
                    item_date = item.date.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    msg.body += f'{item.description} {item_date}\n'

                    mail.send(msg)
                    print("mail sent!!")
            else:
                print(str(datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S')) +
                    ' No new expired item ' + str(user.id))
