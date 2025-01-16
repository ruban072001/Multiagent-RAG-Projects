from youtubesearchtool import YouTubeSearchTool
from Addvideotovector import AddVideoToDBTool
from crewai import Agent, Crew, Task, Process
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Type, Optional
from crewai_tools import FirecrawlSearchTool, RagTool

load_dotenv()


class ContentCreaterInfo(BaseModel):
    first_name: str = Field(
        ..., description= "First name of the content creator"
    )
    last_name: Optional[str] = Field(
        None, description= "last name of the content creator"
    )
    main_topics_covered: Optional[List[str]] = Field(
        None, description="The main topics covered by the content creator"
    )
    bio: Optional[str] = Field(
        None, description="A brief biography of the content creator"
    )
    email_address: Optional[str] = Field(
        None, description="The email address of the content creator"
    )
    linkedin_url: Optional[str] = Field(
        None, description="The LinkedIn profile URL of the content creator"
    )

    
youtube_search_tool = YouTubeSearchTool()
add_video_to_db = AddVideoToDBTool()
web_search_tool = FirecrawlSearchTool()
rag_tool = RagTool()