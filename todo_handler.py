from pathlib import Path
import logging
import aiofiles
import asyncio
from ignore import Ignore

class TodoHandler:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.logger = logging.getLogger(__name__)

    async def read_file(self, file_path):
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                return file_path, await file.read()
        except UnicodeDecodeError as e:
            self.logger.error(f"Failed to decode {file_path}: {e}")
            return file_path, None 
    
    async def fetch_files(self):
        tasks = []
        ignore = Ignore()

        for file_path in self.repo_path.rglob('*'):
            if '.git' in str(file_path):
                continue
            
            if ignore.is_ignored(file_path):
                continue

            if file_path.is_file():
                tasks.append(self.read_file(file_path))

        results = await asyncio.gather(*tasks) 
        for content in results:
            if content is not None:
                print(f"Contents of file: {content[1]}")
            else:
                print("Could not read a file due to encoding issues.")