from typing import Any
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.db.models.query import QuerySet
from django.views.generic import (ListView, UpdateView, DeleteView)
from .forms import VideoForm
from .models import Video
from mpesa.models import Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden



def index(request):
    videos = Video.objects.all()
    return render(request, "videos/index.html", {"videos": videos})

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    return render(request, 'videos/detail.html', {'object': video})

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            print("is valid ?????", form.is_valid())
            form.instance.user = request.user
            form.save()
            return redirect('videos-home')
        else:
            messages.warning(request, "error occured")

    else:
        form = VideoForm()

    return render(request, 'videos/video_form.html', {'form': form})


class UserVideoListView(ListView):
    model = Video
    # <app>/<model>_<view_type.html
    template_name = 'videos/user_videos.html'
    context_object_name = 'videos'
    paginate_by = 6

    def get_queryset(self) -> QuerySet[Any]:
        user = get_object_or_404(
            User, username=self.kwargs.get('username'))
        return Video.objects.filter(user=user).order_by('-upload_date')


class VideoListView(ListView):
    model = Video
    # <app>/<model>_<view_type.html
    template_name = 'videos/home.html'
    context_object_name = 'videos'
    ordering = ['-upload_date']


class VideoUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'videos/video_form.html'

    def form_valid(self, form):
        # override the form valid method to use custom validation
        video_file = form.cleaned_data.get('video_file')
        if video_file._file != None:

            content_type = video_file.content_type.split('/')[0]
            if content_type not in ['video']:
                form.add_error('video_file', _('File is not a video'))
                return self.form_invalid(form)
        if video_file._file == None:
            return reverse_lazy('videos-home')

        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.save()
        return response

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.user

    def get_success_url(self):
        return reverse_lazy('videos-home')


class VideoDeleteView(
    LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
    model = Video
    success_url = '/'

    def test_func(self) -> bool | None:
        video = self.get_object()
        if self.request.user == video.user:
            return True
        else:
            return False


@login_required
def video_playback(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    # Check if the current user has paid for the video
    if request.user != video.user:
        if not has_paid(request.user, video):
            return HttpResponseForbidden(
                "You have not paid for this video.")

    return render(
        request, 'videos/video_playback.html', {'video': video})

def has_paid(user, video):
    # Check if the user has a paid transaction for the given video
    return Transaction.objects.filter(
        phone_number=user.profile.phone_number,
        video=video, status='successful').exists()


def video_search(request):
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['q']
        # Filter your model by the search query
        videos = Video.objects.filter(
            title__icontains=search_query) | Video.objects.filter(
                description__icontains=search_query)
        users = User.objects.filter(username__icontains=search_query)
        result_count = videos.count()
        featured_video = Video.objects.first()
        context = {
            'query':search_query,
            'videos': videos,
            'users': users,
            'result_count': result_count,
            'featured_video': featured_video
        }
        print(vars(users))
        return render(request, 'videos/video_search.html', context)
    else:
        return render(request, 'videos/video_search.html',{})
