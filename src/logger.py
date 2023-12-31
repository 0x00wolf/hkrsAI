import os
import re
import json
from typing import Type
from src.pathfinder import PathFinder
from src.conversation import Conversation


class Logger:
    def __init__(self, paths: PathFinder, log_level: int, log_format: str):
        """Logs conversations and saves data at the user's request"""
        self.level: int = log_level
        self.format: str = log_format
        self.paths: Paths = paths
        self.number: int = 0
        self.file: str = ''
        self.savefile: str = ''
        self.save_number: int = 0
        self.new_log()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_value: int):
        if 1 != new_value != 2:
            raise TypeError
        else:
            self._level = new_value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, new_value: str):
        if new_value == 'txt' or new_value == 'json':
            self._format = new_value
        else:
            self._format = new_value

    def new_log(self):
        self.number = self._next_number()
        self.file = self._new_file()
        
    def _next_number(self):
        """Fetch the next log number from config.json and updates it"""
        config_data = self._load(self.paths.config)
        self.number = log_num = config_data['log_number']
        config_data['log_number'] = self.number + 1
        self._dump(config_data, self.paths.config)
        return self.number
    
    def _new_file(self):
        """Generates a new logfile relative the current log number"""
        while True:  # to prevent inadvertently overwriting logs if the value is changed in config.json
            self.file = f'{self.paths.logs}/log{self.number}.{self.format}'
            try:
                with open(self.file, 'x'):
                    print(f'[*] logfile generated ~ {self.file}')
                return self.file
            except FileExistsError:
                self.number += 1

    def log(self, conversation: Conversation):
        """Logs the response or messages as a JSON or TXT file relative to args"""
        if self.level == 1 and self.format != 'txt':
            print('[*] level 1 only supports .txt output')
            self.format = 'txt'
        if self.level == 1:
            self._dump(str(conversation.response), self.file)
            return self
        elif self.level == 2 and self.format == 'json':
            self._dump(conversation.messages, self.file)
            return self
        elif self.level == 2 and self.format == 'txt':
            with open(self.file, 'w') as f:
                for i in range(len(conversation.messages)):
                    f.write(f"{conversation.messages[i]['role']}:--------------\n\n" \
                            f"{conversation.messages[i]['content']}\n\n")
                return self

    # >save
    def save(self, arguments, conversation):
        """Saves information at the user's request"""
        if len(arguments) == 0:
            self._update_savefile()
            self._save_text(self.savefile, conversation.reply)
            print(f'[*] saving reply to ~ {self.savefile}')
            return
        if len(arguments) != 2:
            self._update_savefile()
        else:
            self.savefile = arguments[1]
        if arguments[0] == 'code':
            p = re.compile(r"```((.|\n)*)```")
            match = re.search(p, conversation.reply)
            if match:
                self._save_text(self.savefile, match.group())
                print(f'[*] saving code to ~ {self.savefile}')
            else:
                print('[*] error: regex failed.\n[*] ensure that GPT presents code in blocks ```code```')
        if arguments[0] == 'reply':
            self._save_text(self.savefile, conversation.reply)
            print(f'[*] saving reply to ~ {self.savefile}')
        elif arguments[0] == 'response':
            self._save_text(self.savefile, str(conversation.response))
            print(f'[*] saving response to ~ {self.savefile}')

    def _update_savefile(self):
        self.savefile = f'{self.paths.logs}/log{self.number}-{self.save_number}.pktai'
        self.save_number += 1

    @staticmethod
    def _save_text(filename, _text):
        """Simple funtion to save text to a file"""
        with open(filename, 'w') as f:
            f.write(_text)

    @staticmethod
    def _load(json_file):
        """Loads JSON object from a file"""
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def _dump(json_dict, json_file):
        """Dumps a JSON object to a file"""
        with open(json_file, 'w') as f:
            json.dump(json_dict, f, indent=6)
