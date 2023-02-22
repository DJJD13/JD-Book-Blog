import os
import secrets

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from flaskblog import mail


def save_picture(form_picture):
    # Generate random hex for file name, then split the extension from the original name
    # '_' used to 'throw away' variable we won't use
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Gives full path name to picture file name in the profile_pics dir, then save there
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Use Pillow (PIL) to resize image before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    # With sender, need to make sure it isn't sent to spam
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)
