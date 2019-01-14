from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from .. import mail, celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.task
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    with app.app_context():
        mail.send(msg)
