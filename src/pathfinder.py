import os
import json
import sys
import dataclasses


CONFIG_INIT = {'log_number': 0, 'api_key': ''}


class PathFinder:
    """Class that returns an object with necessary paths for runtime operations"""
    def __init__(self, cwd: str):
        self.cwd = cwd
        self.config = f'{self.cwd}/config.json'
        self.logs = f'{self.cwd}/logs'
        self.prompts = f'{self.cwd}/prompts'
        self._first_runtime()
        self._prompts_dir_exists()

    @staticmethod
    def _get_cwd():
        """Fetch the current working directory"""
        abs_path = os.path.abspath(__file__)
        cwd = os.path.dirname(abs_path)
        return cwd

    def _first_runtime(self):
        """Initialize the config.json and logs directory if not present at runtime."""
        self._init_cfg_json()
        self._init_logs_dir()

    def _prompts_dir_exists(self):
        """Check to see if the prompts directory is present, or print an error and exit."""
        if not os.path.exists(self.prompts):
            print('[*] error: prompts directory is missing')
            sys.exit()

    def _init_cfg_json(self):
        """Generate the config.json file."""
        if not os.path.exists(self.config):
            self._dump(CONFIG_INIT, self.config)

    def _init_logs_dir(self):
        """Generate the logs directory"""
        if not os.path.exists(self.logs):
            os.makedirs(self.logs)

    @staticmethod
    def _dump(json_dict, json_file):
        """Dumps a JSON object to a file"""
        with open(json_file, 'w') as f:
            json.dump(json_dict, f, indent=6)
