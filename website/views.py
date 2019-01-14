import base64
from datetime import date

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.datastructures import OrderedSet
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from django.views.generic import TemplateView

from api import senders
from api.models import Event
from website.forms import AttendeeForm


class WelcomeView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_events'] = OrderedSet(Event.objects.filter(eventday__date__gte=date.today()).order_by(
            'eventday__date'))
        context['past_events'] = OrderedSet(Event.objects.filter(eventday__date__lte=date.today()).order_by(
            '-eventday__date'))
        return context


class EventInfoView(TemplateView):
    template_name = 'website/event.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(event=get_object_or_404(Event, slug=context['event']))
        return self.render_to_response(context)


class AttendeeRegistrationView(FormView):
    template_name = 'website/form.html'
    form_class = AttendeeForm

    success_url = '/thanks/'

    def get(self, request, *args, **kwargs):
        event = OrderedSet(Event.objects.filter(slug=kwargs['event'], eventday__date__gte=date.today(),
                                                closed_registration=False))
        if not len(event):
            raise Http404

        event = list(event)[0]

        return self.render_to_response(self.get_context_data(event=event))

    def form_valid(self, form):
        event = OrderedSet(Event.objects.filter(slug=self.request.POST['event'], eventday__date__gte=date.today(),
                                                closed_registration=False))
        if not len(event):
            raise Http404

        event = list(event)[0]

        attendee = form.instance
        attendee.event = event

        try:
            qr_data = senders.send_registration_mail(attendee, event[0])
            context = self.get_context_data(qr_code=base64.b64encode(qr_data).decode('ascii'))
            attendee.save()

            return render(self.request, 'website/thanks.html', context)
        except Exception as e:
            messages.error(self.request, _('Registration failed.'))
            return self.form_invalid(form)

    def form_invalid(self, form):
        event = get_object_or_404(Event, slug=self.request.POST['event'], eventday__date__gte=date.today())
        return self.render_to_response(self.get_context_data(form=form, event=event))
