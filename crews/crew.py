from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os
import json
load_dotenv()


file_path = r"C:\Users\Ruban\Downloads\light-return-449919-s1-0fe95f938030.json"

# Load the JSON file
with open(file_path, 'r') as file:
    vertex_credentials = json.load(file)

# Convert the credentials to a JSON string
vertex_credentials_json = json.dumps(vertex_credentials)

# Search tool
google_tool = SerperDevTool()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    vertex_credentials=vertex_credentials_json
)

@CrewBase
class AgenticCrew():
    """AgenticCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, document_tool, Doc_tool):
        print(Doc_tool)
        if Doc_tool:
            self.tool = document_tool
        else:
            self.tool = google_tool

    @agent
    def retriever(self) -> Agent:
        return Agent(
            config=self.agents_config["retriever"],
            tools=[self.tool],
            verbose=True,
            llm=llm,  # ✅ Ensure correct LLM assignment
            # max_iter=2
        )

    @agent
    def ranker(self) -> Agent:
        return Agent(
            config=self.agents_config["ranker"],
            verbose=True,
            llm=llm,  # ✅ Ensure correct LLM assignment
            # max_iter=2
        )

    @agent
    def responser(self) -> Agent:
        return Agent(
            config=self.agents_config["responser"],
            verbose=True,
            llm=llm,  # ✅ Ensure correct LLM assignment
            # max_iter=2
        )

    @task
    def retriever_task(self) -> Task:
        return Task(
            config=self.tasks_config["retriever_task"],
        )

    @task
    def ranker_task(self) -> Task:
        return Task(
            config=self.tasks_config["ranker_task"],
        )

    @task
    def responser_task(self) -> Task:
        return Task(
            config=self.tasks_config["responser_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgenticCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
