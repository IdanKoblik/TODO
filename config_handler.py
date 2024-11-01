import json
import logging
from pathlib import Path
from typing import Dict, Optional

platforms = {
    1: "Github",
    2: "Gitlab"
}

class ConfigHandler:
    def __init__(self, config_name: str):
        self.config_name = Path(config_name)
        self.logger = logging.getLogger(__name__)

    def load_config(self) -> Optional[Dict[str, str]]:
        try:
            with self.config_name.open('r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.info(f"Configuration file '{self.config_name}' not found. Creating a new one.")
            return self.create_config()

    def create_config(self) -> Optional[Dict[str, str]]:
        try:
            self.logger.info("Please select a platform")
            self.logger.info("[ 1 ] > Github")
            self.logger.info("[ 2 ] > Gitlab")
            try:
                platform = int(input("> "))
                if platform not in platforms:
                    raise ValueError("Invalid platform selection")
    
                host = "github.com"
                if platform == 2:
                    host = input("Enter gitlab host > ")

                token = input("Enter access token > ")
                
                data = {
                    "host": host,
                    "token": token
                }

                with self.config_name.open('w', encoding='utf-8') as config:
                    json.dump(data, config, indent=2)

                return data
            except KeyError:
                self.logger.error("Invalid platform")
                return None
        except Exception as e:
            self.logger.error(f"Error creating configuration file: {e}")
            return None