from typing import List, Type
from embedchain import App
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from embedchain.models.data_type import DataType
from chonkie import SemanticChunker
from dotenv import load_dotenv
load_dotenv

class AddVideoToDBToolInput(BaseModel):
    video_url: str = Field(..., description="The url of the youtube video to add to vector database")
    
class AddVideoToDBToolOutput(BaseModel):
    success: bool = Field(..., description="whether the video added to database or Not")
    
class AddVideoToDBTool(BaseTool):
    name: str = "Add video to Vector DataBase"
    description: str = "With this tool one can able to add video to vector databases"
    args_schema: Type[BaseModel] = AddVideoToDBToolInput
    return_schema: Type[BaseModel] = AddVideoToDBToolOutput
    
    
    def _run(self, video_url: str) -> AddVideoToDBToolOutput:
        
        try:
            app = App()
            app.add(source=video_url, data_type=DataType.YOUTUBE_VIDEO, )
            return AddVideoToDBToolOutput(success=True)
        except Exception as e:
            return AddVideoToDBToolOutput(success=False)



if __name__ == "__main__":
    result = AddVideoToDBTool()._run(video_url="https://www.youtube.com/watch?v=SM66GDRyIVY")
    print(result)