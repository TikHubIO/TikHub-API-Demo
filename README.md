# TikHub API Demo

This repository is a demonstration of how to use the TikHub.io API interface for downloading videos from platforms such as Douyin. Below are the steps for setting up the environment, obtaining the API key, and running the demo scripts.

## 1. Getting Started

### Prerequisites

- Python 3.7+
- [TikHub.io](https://tikhub.io) account (to obtain your API Key)
- TikHub Python SDK (included in the `requirements.txt`)

### Installation

1. Clone this repository:
   
   ```bash
   git clone https://github.com/your-repo/TikHub-API-Demo.git
   cd TikHub-API-Demo
   ```
2. Create and activate a virtual environmen:
   
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/MacOS
   .venv\Scripts\activate      # Windows
   ```
3. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

## 2. Obtaining the API Key

To interact with the TikHub API, you'll need an API Key. You can get it by signing up on [TikHub.io](https://tikhub.io) and navigating to your API dashboard.

Once you have your API Key, create a `.env` file in the root directory of the project and add your key as follows:

```bash
API_KEY=your_private_api_key
```

> ⚠️ Make sure not to commit your `.env` file to version control. The `.gitignore` file in this repository already contains an entry to exclude `.env` files.

## 3. Editing the `.env` file

If the `.env` file does not exist or the `API_KEY` is not set properly, the program will create a default `.env` file for you with a placeholder. You can then edit this file and replace `your_private_api_key` with your actual API Key.

### Example `.env` file

```bash
API_KEY=your_actual_api_key
```

## 4. Running the Demo Scripts

This repository contains two example scripts:

### 1. Douyin Single Video Downloader

File Link: [single_video_downloader.py](https://github.com/TikHubIO/TikHub-API-Demo/blob/main/Douyin/APP%20API%20Demo/single_video_downloader.py)

Download a single video by providing its share URL. You can find the script in the following path:

```bash
APP API Demo/single_video_downloader.py
```

How to run:

```bash
python APP\ API\ Demo/single_video_downloader.py
```

This will fetch and download the video to the `downloads` folder.

### 2. Douyin Profile Videos Downloader

File Link:  [profile_videos_downloader.py](https://github.com/TikHubIO/TikHub-API-Demo/blob/main/Douyin/APP%20API%20Demo/profile_videos_downloader.py)

Download multiple videos from a specific user profile. You can find the script in the following path:

```bash
APP API Demo/profile_videos_downloader.py
```

How to run:

```bash
python APP\ API\ Demo/profile_videos_downloader.py
```

This will download all available videos from the profile to the `downloads` folder.

## 5. License

This project is licensed under the Apache License - see the [LICENSE](https://github.com/TikHubIO/TikHub-API-Demo/blob/main/LICENSE) file for details.
