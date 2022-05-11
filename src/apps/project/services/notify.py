from django.core.mail import EmailMessage
from django.template.loader import get_template
from notifications.signals import notify
from threading import Thread
import logging as log
from django.conf import settings


def send_notify(user, recipient, message, project):
    notify.send(user, recipient=recipient,
                verb=message, action_object=project)
    context_data = {
        'message': message,
        'project': project
    }
    emails = []
    try:
        iter(recipient)
        for r in recipient :
            emails.append(r.email)
    except TypeError:
        emails.append(recipient.email)
    send_email_notification_async(context_data, emails)


def send_email(subject="", html_content="", recipients=[], files=None, from_email=settings.DEFAULT_FROM_EMAIL):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL if from_email is None else from_email
        if subject == "" or html_content == "" or len(recipients) == 0:
            return False
        msg = EmailMessage(subject=subject, body=html_content, from_email=from_email,to=recipients,reply_to=[settings.DEFAULT_FROM_EMAIL])
        msg.content_subtype = "html"  # Main content is now text/html
        if files is not None:
           msg.attach_file(files)
        mail_status = msg.send()
        if mail_status:
            log.info("email send")
            return True, {}
        else:
            log.error("error in sending email.")
            return False, {'message': 'error in sending email.'}
    except Exception as e:
        log.error("Exception: " + str(e))
        return False, {'message': str(e)}


def execute_in_background(function):
    def start_thread(*args, **kwargs):
        thread = Thread(target=function,
                        args=args, kwargs=kwargs)
        thread.start()

    return start_thread


@execute_in_background
def send_email_async(subject="", html_content="", recipients=[], files=None, from_email=settings.DEFAULT_FROM_EMAIL):
    try:
        stat,msg = send_email(subject=subject, html_content=html_content, recipients=recipients, files=files, from_email=from_email)
    except Exception as e:
        log.error("Exception in send_email_async: " + str(e))


def send_email_notification(context_data, recipients=[], files=None):
    try:
        template = get_template("email/project_status_notify.html")

        html = template.render(context_data)
        mail_status, response = send_email(subject='[Гранты главы РС(Я)] ' + context_data['message'], html_content=html, recipients=recipients,
                                           files=None, from_email=settings.DEFAULT_FROM_EMAIL)
    except Exception as e:
        log.error("Exception in send_email_notification: " + str(e))


@execute_in_background
def send_email_notification_async(context_data, recipients=[], files=None):
    try:
        send_email_notification(context_data, recipients, files)
        log.info(f"mail sent to {recipients}")

    except Exception as e:
        log.error("Exception in send_email_notification_async:" + str(e))

        return False