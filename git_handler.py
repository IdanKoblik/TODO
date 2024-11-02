import logging
import configparser
from pathlib import Path
import os 

class GitHandler():
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.logger = logging.getLogger(__name__)
        self.git_config = configparser.ConfigParser()

    def is_valid_repo(self) -> bool:
        return (self.repo_path / '.git').is_dir()
    
    def get_git_repo_path(self) -> Path:
        return self.repo_path / '.git'

    