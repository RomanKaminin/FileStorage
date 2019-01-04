import django_filters
from app.models import File
from django.utils.translation import ugettext_lazy as _


class FileFilter(django_filters.FilterSet):

    class Meta:
        model = File
        fields = ['date',]

    def __init__(self, *args, **kwargs):
        super(FileFilter, self).__init__(*args, **kwargs)
        self.filters['date'].label = _("Дата создания")


