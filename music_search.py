from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json, time, sys
#import pandas as pd

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results,
        order="viewCount"
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of matching videos.
    # Filter out channels, and playlists
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["playlistId"]))

    with open("raw.txt", "w") as f:
        json.dump(search_response, f, indent=4, sort_keys=True)

    write_to_file(options.q, videos, channels, playlists)

def write_to_file(search_term, videos, channels, playlists):

    f = open("all_results.txt", "w")
    stg = "\n\nYoutube results for search \'" + search_term + "\' at " + time.strftime("%m/%d/%Y %H:%M:%S") + "\nVideos\n----------\n"
    stg = stg.encode("utf-8")
    f.write(stg)
    f.close()
    for i in xrange(len(videos)):
        with open("all_results.txt", "a") as f:
            stg = str(i+1)+".".encode("utf-8")
            f.write(stg)
            for line in videos[i]:
                stg = u" ".join(word for word in line).encode("utf-8")
                f.write(stg)
            # stg = u"\n".encode("utf-8")
            # f.write(stg)
        f = open("all_results.txt", "a")
        stg = " http://www.youtube.com/watch?v=" + videos[i][videos[i].index("(")+1:videos[i].index(")")] + "\n"
        stg = stg.encode("utf-8")
        f.write(stg)
        f.close()

    f = open("all_results.txt", "a")
    stg = "\nChannels\n----------\n"
    stg = stg.encode("utf-8")
    f.write(stg)
    f.close()
    for i in xrange(len(channels)):
        with open("all_results.txt", "a") as f:
            stg = str(i+1)+".".encode("utf-8")
            f.write(stg)
            for line in channels[i]:
                stg = u" ".join(word for word in line).encode("utf-8")
                f.write(stg)
            stg = u"\n".encode("utf-8")
            f.write(stg)

    f = open("all_results.txt", "a")
    stg = "\nPlaylists\n----------\n"
    stg = stg.encode("utf-8")
    f.write(stg)
    f.close()
    for i in xrange(len(playlists)):
        with open("all_results.txt", "a") as f:
            stg = str(i+1)+".".encode("utf-8")
            f.write(stg)
            for line in playlists[i]:
                stg = u" ".join(word for word in line).encode("utf-8")
                f.write(stg)
            stg = u"\n".encode("utf-8")
            f.write(stg)

    

if __name__ == "__main__":
    # for command line args
    # print " ".join(x+" " for x in sys.argv[1:])
    # params = " ".join(x+" " for x in sys.argv[1:])
    # change the default param to what ever you want to search
    argparser.add_argument("--q", help="Search term", default="music")
    # default number of result you want
    argparser.add_argument("--max-results", help="Max results", default=40)
    args = argparser.parse_args()

    try:
        youtube_search(args)
    except HttpError, e:
        print "An HTTP error %d occured:\n%s" % (e.resp.status, e.content)
