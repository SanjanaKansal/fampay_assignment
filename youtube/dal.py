from datetime import datetime
import pytz

from youtube import models
from django.db.models import Q


def save_videos(videos_data):
	if not videos_data['items']:
		return
	for item in videos_data['items']:
		video = models.YoutubeVideo.objects.filter(video_id=item['id']['videoId'])
		if not video:
			snippet = item['snippet']
			thumbnails = snippet['thumbnails']
			models.YoutubeVideo.objects.create(
				video_id=item['id']['videoId'],
				title=snippet['title'],
				description=snippet['description'],
				thumbnail_url=thumbnails['default']['url'],
				published_datetime=snippet['publishedAt']
			)


def get_videos_and_sync_token(sync_token, limit=10):
	if not sync_token:
		all_videos = models.YoutubeVideo.objects.order_by('-published_datetime')
	else:
		sync_datetime = datetime.utcfromtimestamp(sync_token).replace(tzinfo=pytz.UTC)
		all_videos = models.YoutubeVideo.objects.filter(
			published_datetime__lt=sync_datetime
		).order_by('-published_datetime')

	videos = list(all_videos.values('video_id', 'title', 'description', 'thumbnail_url', 'published_datetime')[:limit])

	if not videos:
		return None, None

	# Extend Videos
	if all_videos.count() > limit:
		for i in range(min(all_videos.count(), limit)):
			if videos[-1]['published_datetime'].strftime('%s') != all_videos[limit + i].published_datetime.strftime('%s'):
				break
			videos.append(all_videos[limit + i].__dict__)

	new_sync_token = videos[-1]['published_datetime'].strftime('%s')
	return videos, new_sync_token


def search_videos(search_query, limit=10):
	videos = models.YoutubeVideo.objects.filter(
		Q(title=search_query) | Q(description=search_query) | Q(title__contains=search_query) | Q(description__contains=search_query)
	).order_by('-published_datetime')
	return list(videos.values('video_id', 'title', 'description', 'thumbnail_url', 'published_datetime')[:limit])


