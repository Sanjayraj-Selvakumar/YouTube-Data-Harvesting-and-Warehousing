import mysql.connector
def connection_to_mysql():
    connection = mysql.connector.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        password = "1234",
        database = "youtube_warehouse"
    )
    return connection

import googleapiclient.discovery
api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyCTQm0nVQpRBGsum52vUCmOdvPAfHEYUVw"
youtube = googleapiclient.discovery.build(api_service_name,api_version,developerKey=api_key)

def channel_information(chnid):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=chnid
    )
    Channel_Info = request.execute()
    channel_data = dict(channel_id = Channel_Info['items'][0]['id'],
                        channel_name = Channel_Info['items'][0]['snippet']['title'],
                        channel_Description = Channel_Info['items'][0]['snippet']['description'],
                        channel_views = Channel_Info['items'][0]['statistics']['viewCount'])
    return channel_data

def playlist_details(Chl_id):
    PL_data=[]
    next_page_token=None
    while True:
        request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=Chl_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for i in response['items']:
            data = dict(Playlist_id = i['id'],
                           channel_id_playlist = i['snippet']['channelId'],
                           Playlist_name = i['snippet']['title'])
            PL_data.append(data)
        next_page_token=response.get('nextPageToken')
        if next_page_token is None:
            break
    return PL_data

def Video_id_details(chn_id):
    while True:
        request = youtube.channels().list(
                part="contentDetails",
                id=chn_id
            )
        Video_details = request.execute()
        Vid_Playlist = Video_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token=None
        Video_id = []
        Video_details1 = youtube.playlistItems().list(
                                                part='snippet',
                                                playlistId=Vid_Playlist,
                                                maxResults=50,
                                                pageToken=next_page_token).execute()
        for i in range(len(Video_details1['items'])):
            Video_id.append(Video_details1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=Video_details1.get('nextPageToken')
        if next_page_token is None:
            break
    return Video_id

def duration_convert(duration_st):
    duration_str = duration_st[2:]
    minutes = 0
    seconds = 0
    if 'M' in duration_str:
        minutes, duration_str = duration_str.split('M')
        minutes = int(minutes)
    if 'S' in duration_str:
        seconds = int(duration_str.rstrip('S'))

    total_seconds = minutes * 60 + seconds
    return total_seconds

def Video_data(chn):
    v_ids = Video_id_details(chn)
    Video_datas=[]
    for v_id in v_ids:
        V_details = youtube.videos().list(
                                        part="snippet,contentDetails,statistics",
                                        id=v_id
        )
        Video_details = V_details.execute()
        for Videtails in Video_details['items']:
            Video_list =dict(Vid_id = Videtails['id'],
                            Vid_name = Videtails['snippet']['title'],
                            Vid_Description = Videtails['snippet']['description'],
                            Video_Published_date = Videtails['snippet']['publishedAt'][:len(Video_details['items'][0]['snippet']['publishedAt'])-1],
                            View_count = Videtails['statistics']['viewCount'],
                            Like_count = Videtails['statistics']['likeCount'],
                            Favorite_count = Videtails['statistics']['favoriteCount'],
                            Comment_count = Videtails['statistics']['commentCount'],
                            Duration = duration_convert(Videtails['contentDetails']['duration']),
                            Video_thumbails = Videtails['snippet']['thumbnails']['high']['url'],
                            Caption_status = Videtails['contentDetails']['caption'],
                            Vi_channel_id = Videtails['snippet']['channelId'])
            Video_datas.append(Video_list)
    return Video_datas

def Comment_details(Chen_id):
    Comm_Video_ids = Video_id_details(Chen_id)
    Comment_info =[]
    next_page_token=None
    while True:
        try:
            for i in Comm_Video_ids:
                request = youtube.commentThreads().list(
                    part="snippet,id,replies",
                    videoId=i,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()

                for item in response['items']:
                    Comment_data = dict(comment_id = item['snippet']['topLevelComment']['id'],
                                    v_id = item['snippet']['topLevelComment']['snippet']['videoId'],
                                    comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay'],
                                    author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                    published_date = item['snippet']['topLevelComment']['snippet']['publishedAt'][:len(Video_details['items'][0]['snippet']['publishedAt'])-1])
                    
                    Comment_info.append(Comment_data)
                next_page_token=response.get('nextPageToken')
                if next_page_token is None:
                    break
        except:
            pass
        return Comment_info

import streamlit as st
st.title("Store Data")
channel_link = st.text_input("Enter a Youtube channel link")
button_clicked = st.button("Store data")
Channel_list = []
if button_clicked:
    connection = connection_to_mysql()
    ch_data = channel_information(channel_link)
    Playlist_data = playlist_details(channel_link)
    Videos_data = Video_data(channel_link)
    comment_data = Comment_details(channel_link)
    if ch_data['channel_name'] not in Channel_list:
        Channel_list.append(ch_data['channel_name'])
        cursor = connection.cursor()
        try:
            cursor.execute(f"insert into channel (Channel_id,Channel_Name,channel_Description,channel_views) Values{ch_data['channel_id'],ch_data['channel_name'],ch_data['channel_Description'],ch_data['channel_views']};")
            for i in range(len(Playlist_data)):
                cursor.execute(f"insert into playlist (Playlist_id,Channel_id,Playlist_Name) Values{Playlist_data[i]['Playlist_id'],Playlist_data[i]['channel_id_playlist'],Playlist_data[i]['Playlist_name']};")
            for i in range(len(Videos_data)):
                cursor.execute(f"insert into video (Video_id,Video_Name,Video_Description,Video_Published_date,View_count,Like_count,Favorite_count,Comment_count,Duration,thumbails,Caption_status,channel_id) Values{Videos_data[i]['Vid_id'],Videos_data[i]['Vid_name'],Videos_data[i]['Vid_Description'],Videos_data[i]['Video_Published_date'],Videos_data[i]['View_count'],Videos_data[i]['Like_count'],Videos_data[i]['Favorite_count'],Videos_data[i]['Comment_count'],Videos_data[i]['Duration'],Videos_data[i]['Video_thumbails'],Videos_data[i]['Caption_status'],Videos_data[i]['Vi_channel_id']};")
            for i in range(len(comment_data)):
                cursor.execute(f"insert into comments (Comment_id,Video_id,Comment_text,Comment_author,Comment_published_date) Values{comment_data[i]['comment_id'],comment_data[i]['v_id'],comment_data[i]['comment_text'],comment_data[i]['author_name'],comment_data[i]['published_date']};")     
            connection.commit()
            st.success("Channel data inserted successfully!")
        except mysql.connector.IntegrityError as err:
            if err.errno == 1062:
                st.warning("Channel data already updated in database")
            else:
                st.error(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
    else:
        st.warning("Channel data already updated in database")

if __name__ == '__main__':
    connection = connection_to_mysql()