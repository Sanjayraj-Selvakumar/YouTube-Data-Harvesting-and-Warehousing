import streamlit as st
import googleapiclient.discovery
st.set_page_config(
    page_title="YouTube Data Harvesting and Warehousing "
)

st.title("Youtube channel Info")
st.sidebar.success("Channel Informations")
channel_link = st.text_input("Enter a Youtube channel link")
button_clicked = st.button("Submit")
api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyCTQm0nVQpRBGsum52vUCmOdvPAfHEYUVw"
youtube = googleapiclient.discovery.build(api_service_name,api_version,developerKey=api_key)

if button_clicked:
    request = youtube.channels().list(
    part="snippet,statistics",
    id=channel_link
    )
    response = request.execute()

    YT_Image = response["items"][0]['snippet']['thumbnails']['high']['url']
    YT_Name = response["items"][0]['snippet']['title']
    YT_Sub_count = response["items"][0]['statistics']['subscriberCount']
    YT_Description = response["items"][0]['snippet']['description']
    st.image(YT_Image, use_column_width=True)
    st.write("Channel Name : ",YT_Name)
    st.write("Channel Description : ",YT_Description)
    st.write("Channel Subscriber Count : ",YT_Sub_count)