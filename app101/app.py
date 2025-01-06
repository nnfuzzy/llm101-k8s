import chainlit as cl
from core.logger import logger
from handlers.chat_handler import main
if __name__ == "__main__":
    main()
    logger.info("Application started")