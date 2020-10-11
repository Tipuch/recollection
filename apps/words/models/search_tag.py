from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.words.modelmixins import OwnerMixin
from apps.words.validators import validate_jap_char, validate_eng_char


class SearchTag(OwnerMixin):
    eng_tag = models.CharField(_('English Tag'),
                               max_length=50,
                               blank=True,
                               validators=[validate_eng_char],
                               db_index=True)
    jap_tag = models.CharField(_('Japanese Tag'),
                               max_length=25,
                               blank=True,
                               validators=[validate_jap_char],
                               db_index=True)

    class Meta:
        verbose_name = _('Search Tag')
        unique_together = ('eng_tag', 'jap_tag', 'owner')

    def __str__(self):
        return '{0} {1}'.format(self.eng_tag, self.jap_tag)
