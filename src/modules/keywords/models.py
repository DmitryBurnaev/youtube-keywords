from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token


class TimestampedModel(models.Model):
    """ Base model for providing timestamp info for every record """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Keyword(TimestampedModel):
    """ Stores keywords, linked with django standard users """

    name = models.CharField(_('Name'), max_length=256, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('User'),
                             on_delete=models.CASCADE)

    def __str__(self):
        return '{self.name} [{self.user}]'.format(self=self)

    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')


class VideoItem(TimestampedModel):
    """ Stores given links to youtube videos """

    youtube_id = models.CharField(_('Youtube ID'), primary_key=True,
                                  max_length=32, unique=True)
    title = models.CharField(_('Title'), max_length=256)
    description = models.TextField(_('Description'))
    thumbnail_url = models.CharField(_('Thumbnail Link'), max_length=256)
    published_at = models.DateTimeField(_('Published At'))
    keywords = models.ManyToManyField(Keyword, related_name='videos')

    def __str__(self):
        return self.title[:50]

    def get_link(self):
        return settings.YOUTUBE_LINK_TEMPLATE.format(id=self.youtube_id)

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Video Item')
        verbose_name_plural = _('Video Items')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
