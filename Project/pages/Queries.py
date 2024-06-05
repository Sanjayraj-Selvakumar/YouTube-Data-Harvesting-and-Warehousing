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
import pandas as pd
import streamlit as st
Query = st.selectbox("Select a Query", ["-------Click for Option-------",
                                "What are the names of all the videos and their corresponding channels?",
                                "Which channels have the most number of videos, and how many videos do they have?",
                                "What are the top 10 most viewed videos and their respective channels?",
                                "How many comments were made on each video, and what are their corresponding video names?",
                                "Which videos have the highest number of likes, and what are their corresponding channel names?",
                                "What is the total number of likes for each video, and what are their corresponding video names?",
                                "What is the total number of views for each channel, and what are their corresponding channel names?",
                                "What are the names of all the channels that have published videos in the year 2022?",
                                "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                "Which videos have the highest number of comments, and what are their corresponding channel names?"]
                                )
connection = connection_to_mysql()
cursor = connection.cursor()
if Query=="What are the names of all the videos and their corresponding channels?":
    Ques1 = "select video.Video_Name, channel.Channel_Name from video INNER join channel ON video.Channel_id = channel.Channel_id;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Video Name","ChannelName"])
    st.write(df)
if Query=="Which channels have the most number of videos, and how many videos do they have?":
    Ques1 = "SELECT channel.Channel_Name, COUNT(video.Video_id) AS video_count FROM video INNER JOIN channel ON video.Channel_id = channel.Channel_id GROUP BY video.Channel_id, channel.Channel_Name order by video_count desc limit 1;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["ChannelName","Video Count"])
    st.write(df)
if Query=="What are the top 10 most viewed videos and their respective channels?":
    Ques1 = "SELECT video.Video_Name,channel.Channel_Name from video Inner join channel on video.channel_id = channel.Channel_id order by video.View_count desc limit 10;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Video Name","Channel Name"])
    st.write(df)
if Query=="How many comments were made on each video, and what are their corresponding video names?":
    Ques1 = "select video.Video_Name,count(comments.Comment_id) as Comments_count from comments Inner join video on comments.Video_id=video.Video_id group by video.Video_id, video.Video_Name;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Video Name","Comment Count"])
    st.write(df)
if Query=="Which videos have the highest number of likes, and what are their corresponding channel names?":
    Ques1 = "Select video.Video_Name,channel.Channel_Name from video Inner join channel on video.channel_id = channel.Channel_id order by video.Like_count desc limit 1;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Video Name","Channel Name"])
    st.write(df)
if Query=="What is the total number of likes for each video, and what are their corresponding video names?":
    Ques1 = "select Video_Name,Like_count from video;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Video Name","Like count"])
    st.write(df)
if Query=="What is the total number of views for each channel, and what are their corresponding channel names?":
    Ques1 = "select channel.Channel_Name,sum(video.View_count) as Total_View_Count from video Inner join channel on video.channel_id=channel.Channel_id group by video.channel_id,channel.Channel_Name;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Channel Name","Total View Count"])
    st.write(df)
if Query=="What are the names of all the channels that have published videos in the year 2022?":
    Ques1 = "SELECT video.Video_Name, channel.Channel_Name FROM video INNER JOIN channel ON video.Channel_id = channel.Channel_id WHERE YEAR(video.Video_Published_date) = 2022 ORDER BY video.Video_Published_date DESC;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Video Name","Channel Name"])
    st.write(df)
if Query=="What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    Ques1 = "SELECT channel.Channel_Name FROM channel INNER JOIN video ON video.Channel_id = channel.Channel_id WHERE YEAR(video.Video_Published_date) = 2022;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Channel Names of videos Published in 2022"])
    st.write(df)

if Query=="Which videos have the highest number of comments, and what are their corresponding channel names?":
    Ques1 = "SELECT video.Video_Name, channel.Channel_Name, COUNT(comments.Comment_id) AS Comments_count FROM comments INNER JOIN video ON comments.Video_id = video.Video_id INNER JOIN channel ON video.Channel_id = channel.Channel_id GROUP BY video.Video_id, video.Video_Name, channel.Channel_Name ORDER BY Comments_count DESC limit 1;"
    cursor.execute(Ques1)
    Info = cursor.fetchall()
    df = pd.DataFrame(Info,columns=["Video Name","Channel Name","Comments count"])
    st.write(df)

if __name__ == '__main__':
    connection = connection_to_mysql()