import requests
import chainlit as cl
from chainlit.input_widget import Select, Slider
from langchain_core.messages import HumanMessage
from core.logger import logger
from core.llm import create_llm
from core.graph import create_graph
from config.settings import (
    OLLAMA_HOST,
    current_model,
    temperature,
    max_tokens,
    ollama_models
)

message_history = []


@cl.on_chat_start
async def start():
    logger.info("Starting new chat session")
    cl.user_session.set("graph", create_graph())
    message_history.clear()

    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags")
        #global ollama_models
        ollama_models = sorted([model['name'] for model in response.json()['models']])
        # Using a pre-defined list, because otherwise a long running model is first
        #ollama_models = ["llama3.2:1b", "llama3.2:3b",  "llama3.2:latest", "llama3.3:latest", "mistral:latest", "llama3-groq-tool-use:latest",
        #                 "qwen2.5-coder:32b","paraphrase-multilingual:latest", "nomic-embed-text:latest","mistral:latest",
        #                 "llama3.2-vision:11b", "llama3.2:3b-instruct-fp16","qwq:latest","qwen2:7b" , "all-minilm:latest",
        #                 ]
        current_model = ollama_models[0]
    except Exception as e:
        await cl.Message(
            content="⚠️ Failed to connect to Ollama server",
            author="System"
        ).send()
        return

    await cl.Message(
        content="""# 🤖 Welcome to Ollama Chat Assistant!\n\n
                This is an AI chat interface powered by Chainlit & Ollama models\n,
                Please check in the options if the default model suits you?\n
                """,
        author="System",
    ).send()

    settings = await cl.ChatSettings([
        Select(
            id="model",
            label="🤖 Model Selection",
            values=ollama_models,
            initial_value=current_model
        ),
        Slider(
            id="temperature",
            label="🌡️ Temperature",
            initial=temperature,
            min=0,
            max=1,
            step=0.1
        ),
        Slider(
            id="max_tokens",
            label="📝 Max Tokens",
            initial=max_tokens,
            min=100,
            max=2000,
            step=100
        )
    ]).send()

    llm = create_llm(current_model, temperature, max_tokens)
    cl.user_session.set("llm", llm)

    await cl.Message(
        content="✨ System is ready! You can start chatting now.",
        author="System"
    ).send()


@cl.on_settings_update
async def setup_agent(settings):
    global current_model, temperature, max_tokens

    current_model = settings["model"]
    temperature = float(settings["temperature"])
    max_tokens = int(settings["max_tokens"])

    llm = create_llm(current_model, temperature, max_tokens)
    cl.user_session.set("llm", llm)


@cl.on_message
async def main(message: cl.Message):
    try:
        logger.info(f"Received message: {message.content}")
        graph = cl.user_session.get("graph")

        current_message = HumanMessage(content=message.content)
        message_history.append(current_message)
        logger.debug(f"Processing message: {current_message}")
        logger.debug(f"Current message history: {message_history}")
        msg = cl.Message(content="Processing...")
        await msg.send()
        async for event in graph.astream({"messages": message_history}):
            logger.debug(f"Received event: {event}")
            for value in event.values():
                logger.info(f"value:{value}")
                if "messages" in value and value["messages"]:
                    response = value["messages"][-1]
                    message_history.append(response)
                    logger.debug(f"Sending response: {response}")
                    await cl.Message(content=response).send()
                    break

    except Exception as e:
        logger.error(f"Error in message handling: {str(e)}", exc_info=True)
        await cl.Message(content="I apologize, but an error occurred. Please try again.").send()