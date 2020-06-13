import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests

from client_credentials import spotify_client_id, oauth_token

def get_liked_artists():
    artist_url = "https://api.spotify.com/v1/me/following"
    response = requests.get(
        artist_url,
        headers = {
            "Authorization":"Bearer " + oauth_token
            })
    artists = response.json()
    return artists

def get_saved_tracks():
    tracks_url = "https://api.spotify.com/v1/me/tracks"
    response = requests.get(
            tracks_url,
            headers = {
                "Authorization":"Bearer " + oauth_token
            })
    tracks = response.json()
    #tracks = json.loads(response.text); 
    #print(response[0])
    print(tracks)
    return tracks 

def youtube_credentials():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": "test1"
            }
        }
    )
    request.execute()
    #print(response)
    return youtube

def music_videos():
    saved_songs = get_saved_tracks()



def main():
    get_saved_tracks()
    #youtube_credentials()


if __name__ == "__main__":
    main()
