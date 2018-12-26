import requests
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

def paginator_work(request, list, num):
    paginator = Paginator(list, num)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    paginator_result = {
        'page_objects': page_obj,
        'paginator':paginator
    }
    return paginator_result


