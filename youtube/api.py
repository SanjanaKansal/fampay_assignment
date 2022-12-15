from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from youtube import dal
from youtube import constants


class YoutubeResource(Resource):
    class Meta:
        resource_name = 'youtube'
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/videos%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_videos'),
                name="api_get_videos",
            ),
            url(
                r"^(?P<resource_name>%s)/video%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('search_videos'),
                name="api_search_videos",
            ),
        ]

    def get_videos(self, request, *args, **kwargs):
        search_query = request.GET.get('q')
        sync_token = int(request.GET.get('sync_token', 0))
        if not search_query or search_query == constants.PREDEFINED_SEARCH_QUERY:
            videos, sync_token = dal.get_videos_and_sync_token(sync_token)
            if not videos:
                return self.create_response(request, {'videos': 'No videos available in DB'})
            return self.create_response(request, {'videos': videos, 'sync_token': sync_token})
        return self.create_response(request, {'videos': 'No videos available in DB'})

    def search_videos(self, request, *args, **kwargs):
        search_query = request.GET.get('q')
        videos = dal.search_videos(search_query)
        return self.create_response(request, {'videos': videos})







