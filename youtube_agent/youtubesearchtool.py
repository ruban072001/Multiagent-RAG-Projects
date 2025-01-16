from typing import List, Type
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests
from dotenv import load_dotenv
import os
load_dotenv()

class YouTubeSearchToolInput(BaseModel):
    channel_handler: str = Field(..., description= "youtube channel handle (eg. @channelhandle)") # channel name
    max_result: int = Field(10, description = "The maximum number of results to return")

class VideoInfo(BaseModel):
    video_id: str
    title: str
    publish_date: datetime
    video_url: str

class YouTubeSearchToolOutput(BaseModel):
    videos: List[VideoInfo]
    
class YouTubeSearchTool(BaseTool):
    name: str = "Youtube Search Tool"
    description: str = ("This tool will helpful for finding youtube videos")
    args_schema: Type[BaseModel] = YouTubeSearchToolInput
    return_schema: Type[BaseModel] = YouTubeSearchToolOutput
    
    def _run(self, channel_handler:str, max_result: int = 10) -> List[YouTubeSearchToolOutput]:
        url = "https://www.googleapis.com/youtube/v3/search"
        param = {
            "part" : "snippet",
            "type" : "channel",
            "q" : channel_handler,
            "key" : os.getenv("YOUTUBE_API_KEY")
        }
        response = requests.get(url=url, params=param)
        response.raise_for_status()
        items = response.json().get("items", [])
        # print(items)
        if not items:
            raise ValueError(f"No channel found for given Handle {channel_handler}")
        
        channel_id = items[0]['id']['channelId']
        
        params = {
            "part" : "snippet",
            "channelId" : channel_id,
            "maxResults" : max_result,
            "order" : "date",
            "type" : "video",
            "key" : os.getenv("YOUTUBE_API_KEY")
        }
        
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])
        
        videos = []
        for item in items:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            publish_date = datetime.fromisoformat(
                item['snippet']['publishedAt'].replace('Z', "+00:00")
                ).astimezone(timezone.utc)
            videos.append(
                VideoInfo(
                    video_id=video_id,
                    title=title,
                    publish_date=publish_date,
                    video_url=f"https://www.youtube.com/watch?v={video_id}"
                )
            )
            
        return YouTubeSearchToolOutput(videos=videos)
        
        
if __name__ == "__main__":
    print(YouTubeSearchTool()._run(channel_handler="@Mr.Beast", max_result=3))