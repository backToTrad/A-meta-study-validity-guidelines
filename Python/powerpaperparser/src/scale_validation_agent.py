"""Scale validation agent for analyzing psychometric scale usage in papers."""

from pathlib import Path
from typing import Any
from typing import Callable
from typing import Literal

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage
from langchain_core.runnables.config import RunnableConfig
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph
from pydantic import BaseModel

from agent_base import BaseAgent
from chat_agent_base import BaseChatState
from chat_agent_base import CallModelNode
from chat_agent_base import ToolExecutorNode
from paper_parser import PaperParser
from scale_validation_tools import ReportScaleValidationTool, SectionReadTool, TableReadTool
from scale_validation_prompt import get_system_prompt, get_scale_validation_prompt
from scale_validation_models import SCALE_CONFIGS
from settings import TARGET_SCALE


class ScaleValidationAgentContext(BaseModel):
    """Context for the Scale Validation agent."""

    paperPath: Path
    result: list[dict[Any, Any]]
    result_path: Path


class AgentState(BaseChatState):
    """State for the Scale Validation agent."""


def from_model_to(state: AgentState) -> Literal["run_tool", "__end__"]:
    """Router function to decide which node to go to next."""
    last_message = state.messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "run_tool"

    return "__end__"


def from_tool_to(state: AgentState) -> Literal["call_model", "__end__"]:
    """Ends if report_scale_validation was called"""
    last_message = state.messages[-1]
    if isinstance(last_message, ToolMessage):
        if last_message.name == "report_scale_validation":
            return "__end__"

    return "call_model"


class ScaleValidationAgent(BaseAgent[ScaleValidationAgentContext]):
    """
    Analyze papers for psychometric scale validation reporting.
    """

    @staticmethod
    def run(ctx: ScaleValidationAgentContext, recursion_limit=300, temperature=0) -> ScaleValidationAgentContext:
        pp = PaperParser(ctx.paperPath)
        
        # Get the scale configuration
        scale_config = SCALE_CONFIGS[TARGET_SCALE]
        
        # Initialize the scale validation reporting tool
        report_tool = ReportScaleValidationTool()
        report_tool.scale_config = scale_config

        tools: list[BaseTool | Callable] = [
            SectionReadTool(paperparser=pp), 
            TableReadTool(paperparser=pp), 
            report_tool
        ]

        # definition of nodes
        call_model = CallModelNode(model_name="gpt-4o", temperature=temperature, tools=tools)
        run_tool = ToolExecutorNode(tools)

        # topology of graph
        graph = StateGraph(AgentState)
        graph.add_node("call_model", call_model)
        graph.add_node("run_tool", run_tool)

        graph.add_conditional_edges("call_model", from_model_to)
        graph.add_conditional_edges("run_tool", from_tool_to)

        graph.set_entry_point("call_model")

        runnable = graph.compile()

        init_state = AgentState(
            messages=[
                SystemMessage(content=get_system_prompt()),
                HumanMessage(
                    content=get_scale_validation_prompt(
                        scale_config=scale_config,
                        title=pp.get_title(), 
                        abstract=pp.get_abstract(),
                        section_index=pp.get_section_index(), 
                        table_index=pp.get_table_index()
                    )
                ),
            ]
        )

        print(init_state.messages[-1])

        ScaleValidationAgent.run_and_report_output(
            runnable,
            init_state,
            config=RunnableConfig(recursion_limit=recursion_limit),
            md_file_name=ctx.result_path
        )

        ctx.result = report_tool.scale_reports

        return ctx
