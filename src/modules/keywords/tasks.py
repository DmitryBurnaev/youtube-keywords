import requests
import logging
import django
django.setup()

from django.conf import settings
from django.db import transaction

from keywords.models import Keyword, VideoItem

log = logging.getLogger(__name__)


def get_last_videos(keyword, raise_error=True):
    """

    :param keyword:
    :param raise_error:
    :return:
    :rtype: dict
    """
    #     'Postman-Token': 'ccaf9fd2-82db-4648-bff3-bb952efa08d2'
    log.info(f'Searching videos for [{keyword}]')
    headers = {
        'Cache-Control': 'no-cache',
    }
    request_body = {
        'type': 'video',
        'part': 'snippet',
        'order': 'date',
        'q': keyword,
        'maxResults': settings.YOUTUBE_API_VIDEOS_COUNT,
        'key': settings.YOUTUBE_API_KEY
    }

    # check response code and coverage this to try block
    response = requests.get(settings.YOUTUBE_API_URL,
                            headers=headers, params=request_body)

    if not response.status_code == 200:
        msg = (f'An HTTP error{response.status_code} '
               f'occurred: {response.content}')
        log.error(msg)
        if raise_error:
            raise LookupError(msg)
        else:
            return {}

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
    keywords = {keyword.name: keyword for keyword in Keyword.objects.all()}
    data_set = {}
    log.info('Start searching for {} keywords'.format(len(keywords)))

    for keyword in keywords:
        last_videos = get_last_videos(keyword, raise_error=False)
        for video_id, video_item in last_videos.items():
            data_set.setdefault(video_id, video_item)
            data_set[video_id].setdefault('keywords', [])
            data_set[video_id]['keywords'].append(keyword)

    exists_items = VideoItem.objects.all()
    given_ids = set(data_set.keys())
    exists_ids = set(exists_items.values_list('youtube_id', flat=True))

    # Add new items
    new_youtube_ids = given_ids - exists_ids
    if new_youtube_ids:
        logging.info(
            'Found {} records to insert'.format(len(new_youtube_ids))
        )
        new_video_items = []
        for youtube_id in new_youtube_ids:
            given_item = data_set[youtube_id]
            new_video_items.append(VideoItem(
                youtube_id=given_item['youtube_id'],
                title=given_item['title'],
                description=given_item['description'],
                thumbnail_url=given_item['thumbnail_url'],
                published_at=given_item['published_at'],
            ))

        new_videos = VideoItem.objects.bulk_create(new_video_items)
        for video_item in new_videos:
            keyword_names = data_set[video_item.youtube_id]['keywords']
            keyword_items = [keywords[k_name] for k_name in keyword_names]
            video_item.keywords.add(*keyword_items)

    log.info('Searching for {} keywords was finished'.format(len(keywords)))


if __name__ == '__main__':
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
    search_and_update_items()
