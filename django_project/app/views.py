from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from filetransfers.api import prepare_upload, public_download_url

from .filtersets import FileFilter
from .forms import FileForm, UserLoginForm, UserRegistrationForm
from .helpers import paginator_work
from .mixin import AjaxLoginMixin, AjaxRegistrationMixin
from .models import File


def delete_handler(request, pk):
    deleted_file = File.objects.get(pk=pk)
    deleted_file.is_deleted = True
    deleted_file.save()
    return redirect("lk")


def create_link_handler(request, pk):
    file_instance = File.objects.get(pk=pk)
    domain = request.build_absolute_uri("/")[:-1]
    file_instance.public_link = domain + file_instance.file.url
    file_instance.save()
    return redirect("lk")


def del_link_handler(request, pk):
    file_instance = File.objects.get(pk=pk)
    file_instance.public_link = ""
    file_instance.save()
    return redirect("lk")


def download_handler(request, pk):
    upload = get_object_or_404(File, pk=pk)
    return public_download_url(request, upload.file)


@login_required(login_url="login")
def upload_handler(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        newfile = File(file=request.FILES["file"])
        upload_url, upload_data = prepare_upload(request, "add_file")
        form.fields["upload_by"].initial = request.user.id
        form.fields["public_link"].initial = upload_url
        form.fields["title"].initial = newfile.file.name
        form.save()
        return redirect("lk")

    upload_url, upload_data = prepare_upload(request, "add_file")
    form = FileForm()
    return render(
        request,
        "upload/upload.html",
        {"form": form, "upload_url": upload_url, "upload_data": upload_data},
    )


class HomePageView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegisterView(AjaxRegistrationMixin, FormView):
    form_class = UserRegistrationForm
    template_name = "registration/registration.html"
    success_url = "/lk/"


class LoginView(AjaxLoginMixin, FormView):
    form_class = UserLoginForm
    template_name = "registration/login.html"
    success_url = "/lk/"


class PersonalArea(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "lk.html"
    model = File
    filter_class = FileFilter

    def get_context_data(self, **kwargs):
        qs = self.model.objects.filter(upload_by=self.request.user.id, is_deleted=False)
        if qs.exists():
            filtered = self.filter_class(self.request.GET, queryset=qs)
            params = self.request.GET.copy()
            if "page" in params:
                del params["page"]
            list_groups = []
            for g in self.request.user.groups.all():
                list_groups.append(g.name)

            qs_with_filters = filtered.qs
            paginator = paginator_work(
                self.request, qs_with_filters.order_by("-date"), 5
            )
            params = self.request.GET.copy()
            if "page" in params:
                del params["page"]
            context = {
                "paginator": paginator["paginator"],
                "page_objects": paginator["page_objects"],
                "params": urlencode(params),
                "filter": filtered,
            }
        else:
            context = {}
        return context


def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect("/")
