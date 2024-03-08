from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
from urllib.parse import urlparse, parse_qs


def get_video_id(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract query parameters
    query_params = parse_qs(parsed_url.query)

    # Extract the video ID
    video_id = query_params["v"][0]

    return video_id


def extract_transcript(url):
    video_id = get_video_id(url)
    data = yta.get_transcript(video_id)
    transcript = ''
    for value in data:
        for key, val in value.items():
            if key == 'text':
                transcript += val

    lines = transcript.splitlines()
    final_text = ' '.join(lines)
    return final_text


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=ha-O5YYVzNo&ab_channel=ETCGExperiments"
    print(extract_transcript(url))
