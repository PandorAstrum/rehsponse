from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rehsponse import models
from rehsponse.forms import RehsponseModelForm, UserModelForm
from rehsponse.mixins import FormUserNeededMixin, UserOwnerMixin


# USER =====================================================
class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "user/user_detail.html"
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDetailView, self).get_context_data(object_list=None, **kwargs)
        _username = self.kwargs.get('username')
        context['user_url'] = get_object_or_404(models.UserProfile, username__iexact=_username)
        return context

    def get_object(self, queryset=models.UserProfile):
        _username = self.kwargs.get('username')
        obj = get_object_or_404(models.UserProfile, username__iexact=_username)
        return obj


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """"""
    queryset = models.UserProfile.objects.all()
    form_class = RehsponseModelForm
    template_name = "user/user_edit.html"
    success_url = '/'

    def get_object(self, queryset=models.UserProfile):
        _username = self.kwargs.get('username')
        obj = get_object_or_404(models.UserProfile, username__iexact=_username)
        return obj


# REHSPONSE ================================================
class RehsponseListView(LoginRequiredMixin, ListView):
    """All Response View (RETRIEVE LIST)"""
    template_name = "rehsponse/rehsponse_list.html"
    login_url = "/login/"

    def get_queryset(self, *args, **kwargs):
        """Query mixin"""
        qs = models.Rehsponse.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(rehsponse_text__icontains=query) |
                Q(user_profile__first_name__icontains=query) |
                Q(user_profile__last_name__icontains=query)
            )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        """Context mixin"""
        context = super(RehsponseListView, self).get_context_data(object_list=None, **kwargs)
        context['create_form'] = RehsponseModelForm()
        context['create_url'] = reverse_lazy('create')
        return context


class RehsponseCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
    """Create A Response (CREATE)"""
    form_class = RehsponseModelForm
    template_name = "rehsponse/forms/create_rehsponse_form.html"
    success_url = "/"
    login_url = "/login/"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RehsponseCreateView, self).get_context_data(object_list=None, **kwargs)
        context['btn_title'] = "Rehsponse"
        return context


class RehsponseReplyView(LoginRequiredMixin, View):
    """Reply view"""
    def get(self, request, pk, *args, **kwargs):
        reply = get_object_or_404(models.Rehsponse, pk=pk)
        if request.user.is_authenticated:
            new_reply = models.Rehsponse.objects.respond(request.user, reply)
            return HttpResponseRedirect(new_reply.get_absolute_url())
        return HttpResponseRedirect(reply.get_absolute_url())


class RehsponseDetailView(LoginRequiredMixin, DetailView):
    """A single Response view (RETRIEVE)"""
    template_name = "rehsponse/rehsponse_detail.html"
    login_url = "/login/"

    def get_object(self, queryset=models.Rehsponse):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(models.Rehsponse, pk=pk)
        return obj


class RehsponseUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    """Edit a response"""
    queryset = models.Rehsponse.objects.all()
    form_class = RehsponseModelForm
    template_name = "rehsponse/forms/update_rehsponse_modal_form.html"
    success_url = '/'


class RehsponseDeleteView(LoginRequiredMixin, UserOwnerMixin, DeleteView):
    """Delete a Response"""
    model = models.Rehsponse
    template_name = "rehsponse/forms/delete_rehsponse_modal_form.html"
    success_url = reverse_lazy("home")


# HASH TAGS =================================================================
class HashTagView(View):
    """Hash Tags simple view"""
    def get(self, request, hashtag, *args, **kwargs):
        obj, created = models.HashTag.objects.get_or_create(tag=hashtag)
        return render(request, 'hashtags/tag_detail.html', {'obj': obj})


# CONTACT ===================================================================
class ContactListView(ListView):
    """Contact simple view (LIST)"""
    template_name = "contacts.html"
    model = models.Contact


class AuthView(ListView):
    """Base login page"""
    template_name = "login.html"

    def get_queryset(self):
        """Query mixin"""
        return None
