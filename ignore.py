import subprocess

class Ignore:
    @staticmethod
    def is_file_ignored(file_path):
        try:
            result = subprocess.run(
                ['git', 'check-ignore', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            return result.returncode == 0
        except FileNotFoundError:
            print("Git is not installed or the command cannot be found.")
            return False