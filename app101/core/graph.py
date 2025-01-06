from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from core.logger import logger
import chainlit as cl

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

async def chatbot(state: State):
    """Process messages and generate response"""
    try:
        logger.debug(f"Received state messages: {state['messages']}")
        llm = cl.user_session.get("llm")
        response = await llm.ainvoke(state["messages"])
        logger.debug(f"LLM response: {response}")
        return {"messages": [response]}
    except Exception as e:
        logger.error(f"Error in chatbot: {str(e)}")
        raise

def create_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.set_entry_point("chatbot")
    return graph_builder.compile()