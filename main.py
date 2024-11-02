import logging
import sys
from pathlib import Path
from git_handler import GitHandler
from config_handler import ConfigHandler
from todo_handler import TodoHandler
import asyncio
from github import *

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_repo_path() -> Path:
    if len(sys.argv) != 2:
        raise ValueError("Usage: python3 main.py <path-to-git-project>")
    return Path(sys.argv[1]).expanduser()

async def initialize_handlers(repo_path: Path) -> tuple[GitHandler, ConfigHandler, TodoHandler]:
    git_handler = GitHandler(repo_path)
    if not git_handler.is_valid_repo():
        raise ValueError(f"The git repository directory '{repo_path}' was not found.")

    config_handler = ConfigHandler(git_handler, 'config.json', repo_path)
    config, todo_handler = config_handler.load_config()
    if config is None:
        raise ValueError("Failed to load or create configuration.")

    return git_handler, config_handler, todo_handler 

async def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)

    #TODO: [test] - [test]  (https://github.com/IdanKoblik/TODO/issues/33)

    try:
        repo_path = get_repo_path()
        git_handler, config_handler, todo_handler = await initialize_handlers(repo_path)

        await todo_handler.fetch_files()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
