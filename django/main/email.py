"""
    Handling of token links creation and sending emails
"""

# for generating of activation/token links
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
import enum

# for sending mails
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

class TokenLinkType(enum.Enum):
    mail_activation = 1
    account_deletion = 2
    password_change = 3
    email_change = 4


class TokenGenerator(PasswordResetTokenGenerator):

    def __init__(self, token_link_type=TokenLinkType.mail_activation):
        self.type = token_link_type

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active) + six.text_type(self.type)
        )


account_activation_token = TokenGenerator(TokenLinkType.mail_activation)
account_deletion_token = TokenGenerator(TokenLinkType.account_deletion)
password_change_token = TokenGenerator(TokenLinkType.password_change)
email_change_token = TokenGenerator(TokenLinkType.email_change)


class MailSender:

    def __init__(self, template_path='emails/base.html'):
            self.EMAIL_TEMPLATE = get_template(template_path)

    def __call__(self, subject, message, to_email, link=None):
        message = self.EMAIL_TEMPLATE.render(
            {
                'message' : message, 
                'link' : link, 
            }
        )
        email = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [to_email])
        email.attach_alternative(message, "text/html")
        email.send()


send_mail = MailSender()
