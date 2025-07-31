from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai.tools import BaseTool


class FileWriterTool(BaseTool):
    name: str = "file_writer"
    description: str = "Writes content to a file."

    def _run(self, file_name: str, content: str, directory: str = "."):
        import os
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Written to {file_path}"


file_writer_tool_summary = FileWriterTool()
file_writer_tool_action_items = FileWriterTool()
file_writer_tool_sentiment = FileWriterTool()



@CrewBase
class MeetingMinutesCrew:
    """Meeting Minutes Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def meeting_minutes_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config["meeting_minutes_summarizer"],  # type: ignore[index]
            tools=[file_writer_tool_summary, file_writer_tool_action_items, file_writer_tool_sentiment]
        )

    @agent
    def meeting_minutes_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["meeting_minutes_writer"],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def meeting_minutes_summarizer_task(self) -> Task:
        return Task(
            config=self.tasks_config["meeting_minutes_summarizer_task"],  # type: ignore[index]
        )

    @task
    def meeting_minutes_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config["meeting_minutes_writer_task"],  # type: ignore[index]
        )


    
    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
