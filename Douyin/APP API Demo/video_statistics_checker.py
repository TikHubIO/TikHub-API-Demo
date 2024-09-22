import os
import asyncio
import httpx
import aiofiles
from tikhub import Client
from dotenv import load_dotenv

# 加载 .env 文件 | Load .env file
load_dotenv()

# 从环境变量中获取 API_KEY | Get API_KEY from environment variables
api_key = os.getenv("API_KEY")

if not api_key or api_key == "your_private_api_key":
    # 检查并创建默认的 .env 文件 | Check and create default .env file
    async def create_default_env_file():
        async with aiofiles.open(".env", "w") as file:
            await file.write("API_KEY=your_private_api_key")
        raise ValueError("API_KEY is not set in .env file")


    asyncio.run(create_default_env_file())

# 初始化 TikHub 客户端 | Initialize TikHub client
client = Client(api_key=api_key)


# 获取视频统计信息 | Get video statistics
async def video_statistics_checker(video_url: str):
    try:
        video_info = await client.DouyinAppV3.fetch_one_video_by_share_url(video_url)

        aweme_id = video_info["data"]["aweme_detail"]["aweme_id"]
        statistics_1 = video_info["data"]["aweme_detail"]["statistics"]

        statistics_2 = await client.DouyinAppV3.fetch_video_statistics(aweme_id)

        all_statistics = statistics_1 | statistics_2["data"]["statistics_list"][0]

        return all_statistics
    except KeyError as e:
        print(f"Error retrieving video statistics: {e}")
        return None


# 主函数 | Main function
async def main(video_url: str):
    statistics = await video_statistics_checker(video_url)
    print(statistics)


if __name__ == "__main__":
    video_url = "https://v.douyin.com/e3x2fjE/"
    asyncio.run(main(video_url))
