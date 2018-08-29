from django.conf import settings
from django.db import models

from django.utils.translation import gettext as _


class TimestampedModel(models.Model):
    """ Base model for providing timestamp info for every record """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Keyword(TimestampedModel):
    """ Store keywords, linked with django standard users """

    name = models.CharField(_('Name'), max_length=256)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('User'),
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} [{self.user}]'

    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')

