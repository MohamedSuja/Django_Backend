from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user')
    )
    bio = models.TextField(_('bio'), blank=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
    
    def __str__(self):
        return f"{self.user.email}'s profile"