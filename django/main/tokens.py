from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

import enum


class TokenLinkType(enum.Enum):
    mail_activation = 1
    account_deletion = 2
    password_change = 3


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