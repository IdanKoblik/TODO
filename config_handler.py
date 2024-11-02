import json
import logging
from pathlib import Path
from typing import Dict, Optional
from git_handler import GitHandler
from github import Github
from todo_handler import TodoHandler

platforms = {
    1: "Github",
    2: "Gitlab"
}

class ConfigHandler:
    def __init__(self, git_hadnler: GitHandler, config_name: str, repo_path: Path):
        self.config_name = Path(config_name)
        self.logger = logging.getLogger(__name__)
        self.git_handler = git_hadnler
        self.repo_path = repo_path

    def load_config(self) -> Optional[tuple[Dict[str, str], TodoHandler]]:
        try:
            with self.config_name.open('r', encoding='utf-8') as file:
                body = json.load(file)
                git = None
                if body["platform"] == 1:
                    git = Github(self.git_handler, body["token"])
                else:
                    pass

                todo_handler = TodoHandler(git, self.repo_path)
                return body, todo_handler
            
        except FileNotFoundError:
            self.logger.info(f"Configuration file '{self.config_name}' not found. Creating a new one.")
            return self.create_config()

    def create_config(self) -> Optional[tuple[Dict[str, str], TodoHandler]]:
        try:
            self.logger.info("Please select a platform")
            self.logger.info("[ 1 ] > Github")
            self.logger.info("[ 2 ] > Gitlab")
            try:
                platform = int(input("> "))
                if platform not in platforms:
                    raise ValueError("Invalid platform selection")
                
                token = input("Enter access token > ")

                host = "github.com"
                todoHandler: TodoHandler = None
                if platform == 2:
                    # TODO gitlab - create gitlab impl
                    host = input("Enter gitlab host > ")
                else:
                    github = Github(self.git_handler, token)
                    github.create_label()
                    todoHandler = TodoHandler(github, self.repo_path)

                data = {
                    "platform": platform, 
                    "host": host,
                    "token": token
                }

                with self.config_name.open('w', encoding='utf-8') as config:
                    json.dump(data, config, indent=2)
                
                return data, todoHandler
            except KeyError:
                self.logger.error("Invalid platform")
                return None
        except Exception as e:
            self.logger.error(f"Error creating configuration file: {e}")
            return None