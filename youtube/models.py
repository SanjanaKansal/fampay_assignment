from django.db import models

# Create your models here.


class YoutubeVideo(models.Model):
	video_id = models.CharField(max_length=256, null=False)
	title = models.CharField(max_length=256, null=False)
	description = models.TextField(default='')
	thumbnail_url = models.URLField()
	published_datetime = models.DateTimeField()
