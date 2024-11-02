from pathlib import Path
import logging
import aiofiles
import re
from ignore import Ignore
from git import Git

class TodoHandler:
    def __init__(self, git: Git, repo_path: Path):
        self.repo_path = repo_path
        self.logger = logging.getLogger(__name__)
        self.git = git

    async def handle_file(self, file_path: Path) -> None:
        todos = {}
        todo_pattern = re.compile(r'TODO:\s*\[(.*?)\]\s*-\s*\[(.*?)\]')
        issue_link_pattern = re.compile(r'\(https?://.*?\)')

        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                contents = await file.read()
                lines = contents.splitlines()

                for line in lines:
                    match = todo_pattern.search(line)
                    if match:
                        title, body = match.groups()
                        title, body = title.strip(), body.strip()

                        if issue_link_pattern.search(line):
                            self.logger.info(f"Skipping TODO '{title}' in {file_path.name} as it already has an issue link.")
                            continue

                        todos[title] = body  

            await self.create_issues_and_update_file(file_path, lines, todos)

        except UnicodeDecodeError as e:
            self.logger.error(f"Failed to decode {file_path}: {e}")
        except Exception as e:
            self.logger.error(f"An error occurred while handling {file_path}: {e}")

    async def create_issues_and_update_file(self, file_path: Path, lines: list, todos: dict) -> None:
        for title, body in todos.items():
            self.logger.info(f"Creating new issue for file: {file_path.name} with title: {title}")
            issue = self.git.create_issue(title, body)

            if isinstance(issue, str):
                await self.update_file_with_issue(file_path, lines, title, issue)
            else:
                self.logger.error(f"Unexpected issue response: {issue}")

    async def update_file_with_issue(self, file_path: Path, lines: list, title: str, issue: str) -> None:
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if title in line:
                    line += f" ({issue})" 
                await file.write(line + '\n')  

    async def fetch_files(self) -> None:
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_dir() or '.git' in str(file_path) or Ignore.is_file_ignored(file_path):
                continue
            await self.handle_file(file_path)
