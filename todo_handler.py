from pathlib import Path
import logging
import aiofiles
import re
from ignore import Ignore
from git import *

class TodoHandler:
    def __init__(self, git :Git, repo_path: Path):
        self.repo_path = repo_path
        self.logger = logging.getLogger(__name__)
        self.git = git

    async def handle_file(self, file_path) -> None:
        try:
            todos = {}
            todo_pattern = re.compile(r'TODO:\s*\[(.*?)\]\s*-\s*\[(.*?)\]')
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                async for line in file:
                    match = todo_pattern.search(line)
                    if match:
                        title = match.group(1).strip()
                        body = match.group(2).strip()
                        todos[title] = body  

            for title, body in todos.items():  
                self.logger.info(f"Creating new issue for file: {file_path.name} with title: {title}")
                self.git.create_issue(title, body)  
        except UnicodeDecodeError as e:
            self.logger.error(f"Failed to decode {file_path}: {e}")

    async def fetch_files(self):
        for file_path in self.repo_path.rglob('*'):
            if (file_path.is_dir()):
                continue

            if '.git' in str(file_path) or str(file_path).endswith('.git'):
                continue
            
            if Ignore.is_file_ignored(file_path):
                continue

            if file_path.is_file():
                await self.handle_file(file_path)