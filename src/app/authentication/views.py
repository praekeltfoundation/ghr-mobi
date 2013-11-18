import urlparse

from django.views import generic as generic_views
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_backends
from django.conf import settings
from django.contrib.sites.models import get_current_site, Site, RequestSite
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from registration.views import RegistrationView as BaseRegistrationView

from tunobase.core import mixins as core_mixins

from app.authentication import forms, models

class UpdateProfile(core_mixins.LoginRequiredMixin, generic_views.UpdateView):
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        self.object = form.save()
        
        messages.success(self.request, 'Profile details updated')
        
        return self.render_to_response(self.get_context_data(form=form))
    
class UpdateProfilePassword(core_mixins.LoginRequiredMixin, generic_views.FormView):
    
    def get_form_kwargs(self):
        kwargs = super(UpdateProfilePassword, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        
        messages.success(self.request, 'Password updated.')

        return self.render_to_response(self.get_context_data(form=form))
    
# Registration views

class ProjectRegistration(BaseRegistrationView):
    
    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        registration_profile = models.EndUser.objects.create_user(
            **cleaned_data
        )
        
        return registration_profile
    
    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        return ('registration_complete', (), {})

@csrf_protect
@never_cache
def login(request, template_name='authentication/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=forms.ProjectAuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            the_user = form.get_user()
            
            # Okay, security checks complete. Log the user in.
            backend = get_backends()[0]
            the_user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
            auth_login(request, the_user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            response = HttpResponseRedirect(redirect_to)
                
            return response
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    context.update(extra_context or {})
    
    return render_to_response(
        template_name, 
        context,
        context_instance=RequestContext(request, current_app=current_app)
    )
    
def logout(request, next_page=None,
           template_name='authentication/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)
    
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if redirect_to:
        netloc = urlparse.urlparse(redirect_to)[1]
        # Security check -- don't allow redirection to a different host.
        if not (netloc and netloc != request.get_host()):
            response = HttpResponseRedirect(redirect_to)
            
            return response

    if next_page is None:
        current_site = get_current_site(request)
        context = {
            'site': current_site,
            'site_name': current_site.name,
            'title': 'Logged out'
        }
        if extra_context is not None:
            context.update(extra_context)
        response = TemplateResponse(request, template_name, context,
                                current_app=current_app)
            
        return response
    else:
        # Redirect to this page until the session has been cleared.
        response = HttpResponseRedirect(next_page or request.path)
            
        return response