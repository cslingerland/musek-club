from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, CreateView

from .models import Club, Pick

from datetime import datetime


# Create your views here.
class ClubListView(ListView):
    template_name = 'clubs/clubs.html'
    def get_queryset(self):
        return Club.objects.all()

class ClubView(DetailView):
    model = Club
    template_name = 'clubs/club.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picks'] = Pick.objects.filter(club=self.object).order_by('-created')
        return context
    

class ClubFormView(CreateView):
    model = Club
    template_name = 'clubs/club_form.html'
    fields = [
        'name',
        'tagline',
        'club_type',
        'members'
    ]

    def form_valid(self, form):
        # todo: create logic to pop number if it's already got one at the end
        #       to prevent slug-1-2-3-4 from happening
        slug = slugify(form.cleaned_data['name'])
        counter = 1
        while Club.objects.filter(slug=slug).exists():
            slug = f"{slug}-{counter}"
            counter += 1
        form.instance.slug = slug
        form.instance.create_date = datetime.now()
        return super().form_valid(form)
    

class PickView(DetailView):
    model = Pick
    template_name = 'clubs/pick.html'

class PickFormView(CreateView):
    model = Pick
    template_name = 'clubs/pick_form.html'
    fields = [
        'name',
        'url',
        'reason'
    ]

    # get club and pass into form html
    def get_context_data(self, **kwargs):
        context = super(PickFormView, self).get_context_data(**kwargs)
        context['club'] = Club.objects.get(slug=self.kwargs['slug'])
        return context
    
    # set fields not exposed in the form
    def form_valid(self, form):
        form.instance.club = Club.objects.get(slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        form.instance.created = datetime.now()
        return super().form_valid(form)
    
    # allows for the club slug to be passed to the club url
    def get_success_url(self):
        return reverse_lazy('clubs:club', kwargs={'slug': self.kwargs['slug']})