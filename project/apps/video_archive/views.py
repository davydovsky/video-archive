from typing import List

from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from project.apps.video_archive.forms import VideoFileForm, VideoURLForm
from project.apps.video_archive.models import Video
from project.apps.video_archive.tasks import handle_file_via_url


class VideosListView(View):
    """Main page view for the list of videos and forms."""

    template_name = 'video_archive/video_list.html'

    def get_context_data(self, **kwargs) -> dict:
        """Retrieve context."""
        kwargs['videos_list'] = self._get_videos_list_page()

        if 'video_file_form' not in kwargs:
            kwargs['video_file_form'] = VideoFileForm()
        if 'video_url_form' not in kwargs:
            kwargs['video_url_form'] = VideoURLForm()

        return kwargs

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Render the main page."""
        return render(request, self.template_name, self.get_context_data())

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle forms data."""
        context = {}

        if 'video_file' in request.POST:
            video_file_form = VideoFileForm(request.POST, request.FILES)

            if video_file_form.is_valid():
                video_file = request.FILES.get('video_file')
                if video_file:
                    video = Video(file=video_file)
                    video.save()
                return redirect(reverse('video_archive:video-feed'))
            else:
                context['video_file_form'] = video_file_form

        elif 'video_link' in request.POST:
            video_url_form = VideoURLForm(request.POST)

            if video_url_form.is_valid():
                video_link = request.POST.get('video_link')
                if video_link:
                    handle_file_via_url.delay(video_link)
                return redirect(reverse('video_archive:video-feed'))
            else:
                context['comment_form'] = video_url_form

        return render(request, self.template_name, self.get_context_data(**context))

    def _get_videos_list_page(self) -> Page[List[Video]]:
        """Get videos page according to page."""
        page = self.request.GET.get('page', 1)

        videos_qs = Video.objects.prefetch_related('format_set').order_by('-created')
        paginator = Paginator(videos_qs, 10)
        try:
            videos_list = paginator.page(page)
        except PageNotAnInteger:
            videos_list = paginator.page(1)
        except EmptyPage:
            videos_list = paginator.page(paginator.num_pages)

        return videos_list
