import os

from django.views.generic.base import TemplateView
from .forms import UserRegistrationForm, UserLoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, CreateView
from django.views.generic.edit import FormView
from .mixin import AjaxRegistrationMixin, AjaxLoginMixin
from .models import File
from .helpers import paginator_work
from .filtersets import FileFilter
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.http import Http404

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        File.objects.create_file(uploaded_file.name, request.user.id, fs.url(name))
        context['url'] = fs.url(name)
        return redirect('lk')
    else:
        return render(request, 'upload.html', context)


# class DeleteFileView(DeleteView):
#     model = File
#
#     def get_object(self, queryset=None):
#         os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))
#         obj = super(DeleteFileView, self).get_object()
#         if not obj.upload_by == self.request.user.id:
#             raise Http404
#         return obj

# class UploadFile(CreateView):
#     model = File
#     template_name = 'upload.html'
#     success_url = reverse_lazy('lk')
#
#     def post(self, request, *args, **kwargs):
#         # context = {}
#         uploaded_file = request.FILES['document']
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name, uploaded_file)
#         self.model.objects.create_file(uploaded_file.name, request.user.id, fs.url(name))
#         return redirect(self.success_url)
#         # context['url'] = fs.url(name)
#         # return redirect('lk')

class HomePageView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegisterView(AjaxRegistrationMixin, FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/lk/'


class LoginView(AjaxLoginMixin, FormView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    success_url = '/lk/'


class PersonalArea(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "lk.html"
    model = File
    filter_class = FileFilter

    def get_context_data(self, **kwargs):
        qs = self.model.objects.filter(upload_by=self.request.user.id)
        if qs.exists():
            filtered = self.filter_class(self.request.GET, queryset=qs)
            params = self.request.GET.copy()
            if 'page' in params:
                del params['page']
            list_groups = []
            for g in self.request.user.groups.all():
                list_groups.append(g.name)

            qs_with_filters = filtered.qs
            paginator = paginator_work(self.request, qs_with_filters.order_by('-date'), 5)
            params = self.request.GET.copy()
            if 'page' in params:
                del params['page']
            context = {
                'paginator': paginator['paginator'],
                'page_objects': paginator['page_objects'],
                'params': urlencode(params),
                'filter': filtered,
            }
        else:
            context = {}
        return context


def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

