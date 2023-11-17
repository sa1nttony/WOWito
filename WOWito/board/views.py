from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from .models import Player, Announcement, Response, New
from .filters import PlayerFilter, AnnouncementFilter, PlayerDetailFilter, NewsFilter
from .forms import PlayerForm, AnnouncementForm, SignUpForm, CodeForm, ResponseForm

# Create your views here.


class PlayerView(ListView):
    model = Player
    ordering = 'user__username'
    template_name = 'players.html'
    context_object_name = 'players'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PlayerFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'player_detail.html'
    context_object_name = 'player_detail'
    queryset = Player.objects.all()

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            action = request.POST.get('action')
            response_id = request.POST.get('response_id')
            response = Response.objects.get(id=response_id)
            if action == 'decline':
                response.status = 'DC'
                response.save()
            elif action == 'agree':
                response.status = 'AG'
                response.save()
        return redirect('player_detail', pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['announcements'] = Announcement.objects.all()
        context['responses'] = Response.objects.all()
        return context


class PlayerCreate(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/sign_up.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        Player.objects.create(user=instance, role=form.cleaned_data.get("role"))

        return redirect(self.success_url)


class AnnouncementList(ListView):
    model = Announcement
    template_name = 'announcements.html'
    context_object_name = 'announcements'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AnnouncementFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'announcements_detail.html'
    context_object_name = 'announcements_detail'
    queryset = Announcement.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['responses'] = Response.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            action = request.POST.get('action')
            response_id = request.POST.get('response_id')
            response = Response.objects.get(id=response_id)
            if action == 'decline':
                response.status = 'DC'
                response.save()
            elif action == 'agree':
                response.status = 'AG'
                response.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_create.html'
    success_url = '/announcements/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player'] = Player.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = Player.objects.get(user__username=self.request.user)
        instance.save()

        return redirect(self.success_url)


class AnnouncementUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcement_update.html'


class AnnouncementDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('announcements_list')


class ResponsesList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Response
    template_name = 'responses_list.html'
    context_object_name = 'responses'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            action = request.POST.get('action')
            response_id = request.POST.get('response_id')
            response = Response.objects.get(id=response_id)
            if action == 'decline':
                response.status = 'DC'
                response.save()
            elif action == 'agree':
                response.status = 'AG'
                response.save()
        return redirect('my_account')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PlayerDetailFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['announcements'] = Announcement.objects.all()
        context['player'] = Player.objects.get(user=self.request.user)
        context['filterset'] = self.filterset
        return context


class ResponseCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    model = Response
    form_class = ResponseForm
    template_name = 'response_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['player'] = Player.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = Player.objects.get(user__username=self.request.user)
        id = self.kwargs['pk']
        instance.announcement = Announcement.objects.get(pk=id)
        instance.save()
        return redirect(f'/announcements/{id}')


class ResponseDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('announcements_list')


class NewsList(ListView):
    model = New
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class NewDetail(DetailView):
    model = New
    template_name = 'new_detail.html'
    context_object_name = 'new_detail'
    queryset = New.objects.all()


@login_required
@csrf_protect
def code_form(request):
    player = Player.objects.get(user=request.user)
    form = CodeForm(request=request)
    if request.method == 'POST':
        form = CodeForm(request.POST, request=request)
        if form.is_valid():
            player = Player.objects.get(user=request.user)
            player.confirm()
    return render(request, template_name='code_form.html', context={'form': form, 'player': player})
            # if player.values('auth_code') == code:
            #     player.confirm()
                #TODO дополнить редиректом на страницу с подтверждением правильности кода
                #TODO добавить условие, при котором страницу обновят и в форму выведут "код неверный"


def home_view(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        return render(request, template_name='home.html', context={'player': player})
    else:
        return render(request, template_name='home.html')
