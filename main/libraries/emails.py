from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import activate

from .functions import get_absolute_url
from .tasks import send_email


class EmailBase:
    subject = None
    template_name = None

    def __init__(self, *args, **kwargs):
        pass

    def get_context(self):
        return {
            'title': self.get_subject(),
            'site_url': get_absolute_url(),
            'default_contact_email': settings.DEFAULT_CONTACT_EMAIL,
        }

    def get_subject(self):
        return self.subject

    def get_html_content(self, context):
        return render_to_string(self.template_name, context)

    def send_html_email(self, email_to, context=None, attachments=None, fail_silently=False):
        """
        Send marketing emails to user based on given email_type.
        :param email_to: email of the reciever
        :param context: dict, context to use in email template
        :param attachments: EmailAttachment object or list of them,
        :param fail_silently: Boolean defining if error should be raised in case of fail
        :return: Boolean if sending was successful
        """

        # aktivujeme jazyk pro překlady
        activate('cs')

        # naplníme context
        if not context:
            context = {}
        context.update(self.get_context())

        # vyrenderujeme HTML
        html_content = self.get_html_content(context)

        # odešleme email
        return send_email(subject=self.get_subject(),
                          email_from=settings.DEFAULT_FROM_EMAIL,
                          email_to=email_to,
                          attachments=attachments,
                          html_content=html_content,
                          fail_silently=fail_silently)


class EmailNewOrderToClient(EmailBase):
    subject = 'nová objednávka'
    template_name = 'emails/email_new_order.html'

    def __init__(self, *args, **kwargs):
        super(EmailNewOrderToClient, self).__init__(*args, **kwargs)

    def get_context(self):
        ctx = super(EmailNewOrderToClient, self).get_context()
        return ctx


class EmailFinishedOrder(EmailBase):
    subject = 'dokončená objednávka'
    template_name = 'emails/email_finish_order.html'

    def __init__(self, *args, **kwargs):
        super(EmailFinishedOrder, self).__init__(*args, **kwargs)

    def get_context(self):
        ctx = super(EmailFinishedOrder, self).get_context()
        return ctx


class EmailCancelledOrder(EmailBase):
    subject = 'stornovaná objednávka'
    template_name = 'emails/email_cancel_order.html'

    def __init__(self, *args, **kwargs):
        super(EmailCancelledOrder, self).__init__(*args, **kwargs)

    def get_context(self):
        ctx = super(EmailCancelledOrder, self).get_context()
        return ctx
