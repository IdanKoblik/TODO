import logging
from abc import ABC, abstractmethod
from git_handler import GitHandler

class Git(ABC):
    def __init__(self, gitHandler: GitHandler, token: str):
        self.logger = logging.getLogger(__name__)
        self.token = token
        self.gitHandler = gitHandler

    @abstractmethod
    def create_label(self):
        pass

    @abstractmethod
    def create_issue(self, title: str, description: str):
        pass