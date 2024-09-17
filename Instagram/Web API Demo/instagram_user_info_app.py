import json
import os
import time
import httpx

from dotenv import load_dotenv
from pywebio.input import input, TEXT
from pywebio.output import put_markdown, put_html, put_text, put_row, put_loading, toast, clear, put_button, \
    put_image, use_scope, put_scope, popup, put_file
from pywebio.platform import start_server

# 加载 .env 文件 | Load .env file
load_dotenv()

# 从环境变量中获取 API_KEY | Get API_KEY from environment variables
API_KEY = os.getenv("API_KEY")

if not API_KEY or API_KEY == "your_private_api_key":
    # 检查并创建默认的 .env 文件 | Check and create default .env file
    def create_default_env_file():
        with open(".env", "w") as file:
            file.write("API_KEY=your_private_api_key")
        raise ValueError("API_KEY is not set in .env file")


    create_default_env_file()

# Directory to store downloaded images temporarily
IMG_DIR = './images/'
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)


# Download the profile picture and return the binary content
def download_image(username, image_url):
    # Check if the image had already been downloaded
    if os.path.exists(f"{IMG_DIR}{username}.jpg"):
        with open(f"{IMG_DIR}{username}.jpg", 'rb') as f:
            return f.read()

    # Download the image
    try:
        response = httpx.get(image_url, timeout=10.0)
        if response.status_code == 200:

            # Binary content of the image
            image_content = response.content

            # Save the image to a file
            with open(f"{IMG_DIR}{username}.jpg", 'wb') as f:
                f.write(image_content)

            # Return the binary content of the image
            return image_content
        else:
            return None
    except httpx.RequestError as exc:
        toast(f"An error occurred while downloading image: {exc}", color="error")
        return None


# Fetch user info from API using httpx (synchronous)
def fetch_instagram_user_info(username):
    api_url = f"https://api.tikhub.io/api/v1/instagram/web_app/fetch_user_info_by_username?username={username}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        with httpx.Client(headers=headers, timeout=30) as client:
            response = client.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
    except httpx.RequestError as exc:
        toast(f"An error occurred while requesting: {exc}", color="error")
        return None


# First view: Input view
def input_view():
    with use_scope('input_view', clear=True):
        put_markdown("# Instagram Profile Fetcher")
        put_markdown("Enter Instagram username to fetch profile data and export the data to a CSV/JSON file.")

        # User input
        # API_KEY = input("Enter API Key", type=TEXT, required=True)
        username = input("Enter Instagram Username", type=TEXT, placeholder="Enter Instagram Username", value="instagram", required=True)

        if username:
            show_user_info(username)


# Second view: Display user info
def export_data_view(user_data):
    # Covert the user data to JSON to binary data for download
    binary_user_data = str(json.dumps(user_data)).encode('utf-8')
    now = time.strftime("%Y-%m-%d-%H-%M-%S")
    user_name = user_data.get('username')
    file_name = f"{user_name}_Instagram_Profile_Data_{now}.json"
    popup("Export Data", put_file(file_name, binary_user_data))


def show_user_info(username):
    clear()
    with use_scope('display_view', clear=True):

        data = fetch_instagram_user_info(username)

        # Process and display fetched data
        if data:
            # $.data
            user_data = data['data']

            # Extract necessary info from the JSON response
            followers = user_data.get('edge_followed_by', {}).get('count', 0)
            following = user_data.get('edge_follow', {}).get('count', 0)
            is_private = "Yes" if user_data.get('is_private', False) else "No"
            is_verified = "Yes" if user_data.get('is_verified', False) else "No"
            biography = user_data.get('biography', "")
            profile_pic = user_data.get('profile_pic_url_hd', "")
            media_count = user_data.get('edge_owner_to_timeline_media', {}).get('count', 0)
            user_id = user_data.get('id', "")
            fbid = user_data.get('fbid', "")
            pronouns = ', '.join(user_data.get('pronouns', [])) if user_data.get('pronouns') else "None"
            has_clips = "Yes" if user_data.get('has_clips', False) else "No"
            recent_activity = "Yes" if user_data.get('has_onboarded_to_text_post_app', False) else "No"
            external_url = user_data.get('external_url', 'None')
            highlight_reels = user_data.get('highlight_reel_count', 0)
            video_timeline_count = user_data.get('edge_felix_video_timeline', {}).get('count', 0)
            is_business_account = user_data.get('is_business_account', False)

            # Download the profile picture as binary data
            image_content = download_image(username, profile_pic)

            # Display the data using Markdown and HTML with custom styling
            put_markdown(f"## Instagram Profile Information for **{username}**")
            if image_content:
                put_image(image_content,
                          format='jpg',
                          title=f"{username}'s Profile Picture",
                          width="150px",
                          height="150px",
                          )
            else:
                put_text("Failed to download profile picture.")

            put_markdown(f"""
                        ### User Identity and Profile:
                        * **Username:** {username}
                        * **User ID:** {user_id}
                        * **FBID:** {fbid}
                        * **Biography:** "{biography}"
                        * **Profile Picture Link:** {profile_pic}
                        * **External Links:** {external_url}
                        * **Pronouns:** {pronouns}

                        ### Account Attributes:
                        * **Followers:** {followers} followers
                        * **Following:** {following} users
                        * **Business/Professional Status:** {is_business_account}
                        * **Private Account:** {is_private}
                        * **Verified:** {is_verified}
                        * **Recent Activity:** {recent_activity}

                        ### Content and Media:
                        * **Media Count:** {media_count} media posts on the timeline
                        * **Saved Media:** None
                        * **Video Timeline Count:** {video_timeline_count}
                        * **Highlight Reels:** {highlight_reels}
                        * **Clips Available:** {has_clips}
                        * **Pinned Channels and Collections:** None

                        ### Interactions:
                        No interaction data available.
                        """)
        else:
            toast("No data found or failed to fetch user info. Please try again!", color="error")

        # Buttons for navigation
        put_row([
            put_button("Back", onclick=input_view),
            put_button("Export Data", onclick=lambda: export_data_view(user_data))
        ])


if __name__ == '__main__':
    # Use http://localhost:8080/ to access the app
    start_server(input_view, port=8080)
