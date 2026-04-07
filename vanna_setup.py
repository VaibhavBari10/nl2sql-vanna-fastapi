import os
from dotenv import load_dotenv

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext

from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.google import GeminiLlmService

from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool
)

from vanna.integrations.local.agent_memory import DemoAgentMemory

load_dotenv()

# DEFINE GLOBALS (FIX)
_agent = None
_memory = None


class DefaultUserResolver(UserResolver):
    def resolve_user(self, request: RequestContext) -> User:
        return User(user_id="default_user")


def get_agent():
    global _agent, _memory

    # Return existing instance
    if _agent is not None and _memory is not None:
        return _agent, _memory

    # LLM
    llm = GeminiLlmService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.5-flash"
    )

    # DB
    sqlite_runner = SqliteRunner("clinic.db")

    # Tools
    tool_registry = ToolRegistry()
    tool_registry.tools = [
        RunSqlTool(sqlite_runner),
        VisualizeDataTool(),
        SaveQuestionToolArgsTool(),
        SearchSavedCorrectToolUsesTool()
    ]

    # Memory
    _memory = DemoAgentMemory()

    # User resolver
    user_resolver = DefaultUserResolver()

    # Agent
    _agent = Agent(
        llm,
        tool_registry,
        user_resolver,
        _memory
    )

    return _agent, _memory