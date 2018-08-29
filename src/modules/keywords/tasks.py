import os

import requests
import logging
import django
django.setup()

from django.conf import settings
from django.db import transaction

from keywords.models import Keyword, VideoItem

log = logging.getLogger(__name__)



def get_last_videos(keyword):
    #     'Postman-Token': 'ccaf9fd2-82db-4648-bff3-bb952efa08d2'

    headers = {
        'Cache-Control': 'no-cache',
    }
    request_body = {
        'type': 'video',
        'part': 'snippet',
        'q': keyword,
        'maxResults': settings.YOUTUBE_API_VIDEOS_COUNT,
        'key': settings.YOUTUBE_API_KEY
    }

    # check response code and coverage this to try block
    response = requests.get(settings.YOUTUBE_API_URL,
                            headers=headers, params=request_body)

    if not response.status_code == 200:
        raise LookupError(
            f'An HTTP error{response.status_code} occurred: {response.content}'
        )

    data = response.json()
    data = {
        item['id']['videoId']: {
            'youtube_id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'published_at': item['snippet']['publishedAt'],
            'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
        }
        for item in data['items']
    }
    return data


@transaction.atomic
def search_and_update_items():
    keywords = Keyword.objects.all()
    for keyword in keywords:
        log.info(f'Searching videos for [{keyword.name}]...')
        given_items = get_last_videos(keyword)
        exists_items = VideoItem.objects.all()

        exists_ids = set(exists_items.values_list('youtube_id', flat=True))
        given_ids = set(given_items.keys())

        # Add new items
        new_youtube_ids = given_ids - exists_ids
        if new_youtube_ids:
            logging.info(
                'Found {} records to insert'.format(len(new_youtube_ids))
            )
            new_video_items = []
            for youtube_id in new_youtube_ids:
                # video_item = VideoItem(**given_items[youtube_id])
                # video_item.keywords.add(keyword)
                # new_video_items.append(video_item)
                new_video_items.append(VideoItem(**given_items[youtube_id]))

            new_videos = VideoItem.objects.bulk_create(new_video_items)
            for video_item in new_videos:
                video_item.keywords.add(keyword)

        # Update items
        update_youtube_ids = exists_ids & given_ids
        if update_youtube_ids:
            logging.info(
                'Found {} records to update'.format(len(update_youtube_ids))
            )
            items_to_update = VideoItem.objects.filter(
                youtube_id__in=update_youtube_ids
            )
            for video_item in items_to_update:
                given_item = given_items[video_item.youtube_id]
                video_item['title'] = given_item['title']
                video_item['description'] = given_item['description']
                video_item.keywords.add(keyword)
                video_item.save()

        log.info(f'Searching for [{keyword.name}] was finished')


if __name__ == '__main__':
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
    search_and_update_items()
