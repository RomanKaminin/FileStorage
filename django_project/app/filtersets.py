import django_filters
from app.models import File
from django.utils.translation import ugettext_lazy as _


class FileFilter(django_filters.FilterSet):

    class Meta:
        model = File
        fields = ['title',]

    def __init__(self, *args, **kwargs):
        super(FileFilter, self).__init__(*args, **kwargs)
        self.filters['title'].label = _("Имя файла")


