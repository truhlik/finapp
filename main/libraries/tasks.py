from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def send_email(subject, email_from, email_to, text_content=None, html_content=None,
               attachments=None, fail_silently=False):
    """
    Sends html or plain emails depending on which content is given, attachments must be
    instance of permissions.models.EmailAttachment

    :param subject: String subject of the email
    :param email_to: Email address of the addressee or list of emails
    :param email_from: Email address of the sender
    :param text_content: Plain email content (send only if html_content not given)
    :param html_content: HTML formatted content (send only if text_content not given)
    :param attachments: EmailAttachment object or list of them
    :param fail_silently: Boolean defining if error should be raised in case of fail
    """

    if not isinstance(email_to, list):
        email_to = [email_to]

    if html_content and not text_content:
        text_content = strip_tags(html_content)
    elif text_content and not html_content:
        pass
    else:   # neither text nor html content or both
        raise ImproperlyConfigured("Either text_content or html_content must be given.")

    msg = EmailMultiAlternatives(
        str(subject),
        text_content,
        str(email_from),
        email_to,
    )

    if html_content:
        msg.attach_alternative(html_content, "text/html")

    if attachments:
        from .models import EmailAttachment

        if not isinstance(attachments, list):
            attachments = [attachments]

        for attachment in attachments:
            try:
                if isinstance(attachment, EmailAttachment):
                    msg.attach_file(attachment.path, attachment.mimetype)
            except IOError:
                pass

    return msg.send(fail_silently=fail_silently)

