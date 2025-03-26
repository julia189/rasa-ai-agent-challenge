import googleapiclient.discovery
import os
import oxylabs

api_service_name = "youtube"
api_version = "v3"

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

youtube_client = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = YOUTUBE_API_KEY)
# 'request' variable is the only thing you must change
# depending on the resource and method you need to use
# in your query
request = youtube_client.search().list(
    part = "id,snippet",
    type = 'video',
    q = 'positive birthing stories',
    maxResults=3
)
# Query execution
response = request.execute()
# Print the results
print(response)