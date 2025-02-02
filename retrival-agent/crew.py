from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
load_dotenv()

google_tool = SerperDevTool()

@CrewBase
class AgenticCrew():
	"""AgenticCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
 
	def __init__(self, document_tool):
	
		self.document_tool = document_tool

	@agent
	def retriever(self) -> Agent:
		return Agent(
			config=self.agents_config["retriever"],
			tools=[self.document_tool, google_tool],
			verbose = True
		)

	@agent
	def ranker(self) -> Agent:
		return Agent(
			config=self.agents_config["ranker"],
			verbose = True
		)
        
	@agent
	def responser(self) -> Agent:
		return Agent(
			config=self.agents_config["responser"],
			verbose = True
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
