import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests

from client_credentials import spotify_client_id, oauth_token

def get_saved_tracks():
    tracks_url = "https://api.spotify.com/v1/me/tracks"
    response = requests.get(
        tracks_url,
        headers={
            "Authorization":"Bearer " + oauth_token
        }
    )
    tracks = response.json()
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
    #global youtube
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube

def create_playlist(youtube):
    response = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": "liked songs 3"
            }
        }
    ).execute()
    return response

def add_videos(youtube):
    saved_songs = get_saved_tracks()
    playlist = create_playlist(youtube)
    for obj in saved_songs["items"]:
        artist = obj["track"]["album"]["artists"][0]["name"]
        song = obj["track"]["name"]
        print(artist)
        print(song)
        video = search(youtube, artist + " - " + song)
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist["id"],
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video["items"][0]["id"]["videoId"]
                    }
                }
            }
        ).execute()

def search(youtube, song):
    response = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=song,
        type="video"
    ).execute()
    return response


def main():
    youtube = youtube_credentials()
    add_videos(youtube)


if __name__ == "__main__":
    main()
