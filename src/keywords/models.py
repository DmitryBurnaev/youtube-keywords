from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from django.utils.translation import gettext as _

UserModel = get_user_model()


class Keyword(models.Model):
    """
    Store keywords, linked with django standard users
    """

    name = models.CharField(_('Name'), max_length=256)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   verbose_name=_('Users'))

