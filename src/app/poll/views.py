from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views import generic as generic_views

from tunobase.core import utils as core_utils, mixins as core_mixins
from tunobase.poll import models
from django.contrib import messages
from django.shortcuts import redirect

class PollAnswer(core_mixins.DeterministicLoginRequiredMixin,
        generic_views.FormView):
    """View for handling poll submissions."""

    ajax_template_name = None

    def deterministic_function(self):
        """
        Returns a flag determining if annoymous
        votes are allowed.

        """
        return settings.ANONYMOUS_POLL_VOTES_ALLOWED

    def get_form_kwargs(self):
        """Adds the poll objects to form kwargs."""

        kwargs = super(PollAnswer, self).get_form_kwargs()

        self.poll = core_utils.get_permitted_object_or_404(
            models.PollQuestion, pk=self.kwargs['pk']
        )
        kwargs['poll'] = self.poll

        return kwargs

    def form_valid(self, form):
        """
        If the form is valid and no duplicate votes have
        been cast, save the form.

        """
        cookie_name = 'poll_%s_voted' % self.kwargs['pk']
        form.save(self.request, cookie_name, self.kwargs['pk'])

        if self.request.is_ajax():
            response = core_utils.respond_with_json({
                'success': True,
                'results': render_to_string(
                    self.ajax_template_name, RequestContext(self.request, {
                        'object_list': self.poll.answers\
                                .get_poll_percentages()
                    })
                )
            })
        else:
            response = self.render_to_response(
                self.get_context_data(
                    object_list=self.poll.answers.get_poll_percentages()
                )
            )
        response.set_cookie(cookie_name, True)

        return response

    def form_invalid(self, form):
        """
        Return a list of errors of items that didn't
        pass validation.

        """
        if self.request.is_ajax():
           return core_utils.respond_with_json({
          'success': False,
          'reason': str(form.errors)
           })
        else:
           messages.error(self.request, str(form.errors))
           return redirect(self.request.META['HTTP_REFERER'])


class PollResults(generic_views.ListView):
    """Return the voting results for each poll."""

    def get_queryset(self):
        """Return the voting results for each poll."""
        self.poll = core_utils.get_permitted_object_or_404(
            models.PollQuestion, pk=self.kwargs['pk']
        )

        return self.poll.answers.get_poll_percentages()
