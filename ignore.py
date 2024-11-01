import os
from gitignore_parser import *
from pathlib import Path

class Ignore:
    def __init__(self, gitignore_path='.gitignore'):
        self.gitignore_path = gitignore_path
        self.patterns = self._load_gitignore()

    def _load_gitignore(self):
        if not os.path.isfile(self.gitignore_path):
            raise FileNotFoundError(f"{self.gitignore_path} not found.")

        with open(self.gitignore_path, 'r') as f:
            lines = f.readlines()

        patterns = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
        return patterns

    def is_ignored(self, file_path: Path) -> bool:
        relative_path = str(file_path.relative_to(file_path.anchor))
        for pattern in self.patterns:
            if self._matches_pattern(relative_path, pattern):
                return True
        return False

    def _matches_pattern(self, path: str, pattern: str) -> bool:
        if pattern.endswith('/'):
            return path.startswith(pattern[:-1]) and '/' in path[len(pattern[:-1]):]
        elif '*' in pattern:
            return self._match_with_wildcard(path, pattern)
        else:
            return path == pattern

    def _match_with_wildcard(self, path: str, pattern: str) -> bool:
        pattern_parts = pattern.split('*')
        if not pattern_parts:
            return False
        
        current_index = 0
        for part in pattern_parts:
            if part not in path[current_index:]:
                return False
            current_index = path.index(part, current_index) + len(part)
        
        return True