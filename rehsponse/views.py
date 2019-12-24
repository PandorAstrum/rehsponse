from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rehsponse import models
from rehsponse.forms import RehsponseModelForm, RegistrationModelForm, UserModelForm
from rehsponse.mixins import FormUserNeededMixin, UserOwnerMixin


# USER =====================================================
class UserLoginView(LoginView):
    """Base login page url: /login"""
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = '/'


class UserRegistrationView(FormView):
    """Register a User url: /signup"""
    template_name = 'registration/registration.html'
    form_class = RegistrationModelForm
    success_url = '/login/'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        password = form.cleaned_data.get("password")
        new_user = models.UserProfile.objects.create_user(email=email,
                                                          username=username,
                                                          first_name=first_name,
                                                          last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return super(UserRegistrationView, self).form_valid(form)


class UserPasswordResetView(FormView):
    """Register a User url: /password_reset"""
    template_name = 'registration/pass_reset.html'
    form_class = PasswordResetForm
    success_url = '/login/'


def logout_view(request):
    '''Log out a user url: /logout'''
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/login/')


class UserDetailView(LoginRequiredMixin, DetailView):
    """User profile (RETRIEVE SINGLE) url: /user/<username>/rehsponses"""
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


class UserUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    """Change user profile (PUT, PATCH) url: /user/<username>/edit"""
    template_name = "user/user_edit.html"
    success_url = '/'
    form_class = UserModelForm

    def get_object(self, queryset=models.UserProfile):
        _username = self.kwargs.get('username')
        obj = get_object_or_404(models.UserProfile, username__iexact=_username)
        return obj


# REHSPONSE ================================================
class RehsponseListView(LoginRequiredMixin, ListView):
    """User and responder Response View (RETRIEVE LIST) url: /"""
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


class RehsponseDetailView(LoginRequiredMixin, DetailView):
    """A single Response view (RETRIEVE) url: /rehsponse/<pk>"""
    template_name = "rehsponse/rehsponse_detail.html"
    login_url = "/login/"

    def get_object(self, queryset=models.Rehsponse):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(models.Rehsponse, pk=pk)
        return obj


class RehsponseBoardListView(LoginRequiredMixin, ListView):
    """All Response List url: /board"""
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
        context = super(RehsponseBoardListView, self).get_context_data(object_list=None, **kwargs)
        context['create_form'] = RehsponseModelForm()
        context['create_url'] = reverse_lazy('create')
        return context


class RehsponseCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
    """Create A Response (CREATE) dont need"""
    form_class = RehsponseModelForm
    template_name = "rehsponse/forms/create_rehsponse_form.html"
    success_url = "/"
    login_url = "/login/"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RehsponseCreateView, self).get_context_data(object_list=None, **kwargs)
        context['btn_title'] = "Rehsponse"
        return context
#
#
# class RehsponseReplyView(LoginRequiredMixin, View):
#     """Reply view dont need"""
#     def get(self, request, pk, *args, **kwargs):
#         reply = get_object_or_404(models.Rehsponse, pk=pk)
#         if request.user.is_authenticated:
#             new_reply = models.Rehsponse.objects.respond(request.user, reply)
#             return HttpResponseRedirect(new_reply.get_absolute_url())
#         return HttpResponseRedirect(reply.get_absolute_url())
#
#
# class RehsponseUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
#     """Edit a response dont need"""
#     queryset = models.Rehsponse.objects.all()
#     form_class = RehsponseModelForm
#     template_name = "rehsponse/forms/update_rehsponse_modal_form.html"
#     success_url = '/'
#
#
# class RehsponseDeleteView(LoginRequiredMixin, UserOwnerMixin, DeleteView):
#     """Delete a Response dont need"""
#     model = models.Rehsponse
#     template_name = "rehsponse/forms/delete_rehsponse_modal_form.html"
#     success_url = reverse_lazy("home")


# HASH TAGS =================================================================
class HashTagView(LoginRequiredMixin, View):
    """Hash Tags simple view url: /tags"""
    def get(self, request, hashtag, *args, **kwargs):
        obj, created = models.HashTag.objects.get_or_create(tag=hashtag)
        return render(request, 'hashtags/tag_detail.html', {'obj': obj})


# CONTACT ===================================================================
class ContactListView(ListView):
    """Contact simple view (LIST) url: /contact"""
    template_name = "contacts.html"
    model = models.Contact
