from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, CreateView

from .models import Club, Pick

from datetime import datetime


# Create your views here.
class ClubListView(LoginRequiredMixin, ListView):
    login_url = "/admin"
    template_name = 'clubs/clubs.html'
    def get_queryset(self):
        return Club.objects.filter(members=self.request.user)

class ClubView(LoginRequiredMixin, DetailView):
    model = Club
    template_name = 'clubs/club.html'

    # get and pass in picks related to club
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picks'] = Pick.objects.filter(club=self.object).order_by('-created')
        return context
    
    # ensure user is in club to view it
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user in obj.members.all():
            return obj
        else:
            raise PermissionDenied
    

class ClubFormView(LoginRequiredMixin, CreateView):
    model = Club
    template_name = 'clubs/club_form.html'
    fields = [
        'name',
        'tagline',
        'club_type'
    ]

    def form_valid(self, form):
        # ensure unique slug
        slug = slugify(form.cleaned_data['name'])
        counter = 1
        while Club.objects.filter(slug=slug).exists():
            slug = f"{slug}-{counter}"
            counter += 1
        form.instance.slug = slug
        form.instance.create_date = datetime.now()
        form.save()
        # Auto-add member that created the group
        form.instance.members.add(self.request.user.id)     
        return super().form_valid(form)
    

class PickView(LoginRequiredMixin, DetailView):
    model = Pick
    template_name = 'clubs/pick.html'

class PickFormView(LoginRequiredMixin, CreateView):
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
    