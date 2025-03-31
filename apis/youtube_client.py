import googleapiclient.discovery
import os

api_service_name = "youtube"
api_version = "v3"

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


# 'request' variable is the only thing you must change
# depending on the resource and method you need to use
# in your query



def get_youtube_recommendations(query: str, max_results=3):

    youtube_client = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = YOUTUBE_API_KEY)

    request = youtube_client.search().list(
    part = "id,snippet",
    type = 'video',
    q = query,
    maxResults=max_results,
    videoDuration="long"
    )

    response = request.execute()
    
    return response['items']


def get_text_from_video(video_id: str) -> str:

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        transcript_text = transcript_text.replace("\n", " ").replace("'", "")
        return transcript_text
    except Exception as e:
        return f"Failed to retrieve transcript: {str(e)}"

def create_chunks(transcript_text: str) -> list:
    """
    Split transcript text into processable chunks.

    Args:
        transcript_text (str): Youtube video's transcripted text

    Returns:
        processable chunks
    
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(transcript_text)
    return chunks

get_youtube_recommendations(query='positive birthing stories')
