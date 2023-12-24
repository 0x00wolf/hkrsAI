import openai
import argparse
import variables  # contains help strings and additional resources
import readline
import re
import os
import pathlib
import sys
from platform import system
import subprocess
import json


class ChatGPT:
    """An immutable class wrapper for the ChatGPT API with values set to their defaults."""
    def __init__(self):
        self.client = None  # client = openai.OpenAI(api_key="<INSERT_API_KEY")
        self.model = 'gpt-3.5-turbo'
        self.temperature = 0.7
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.0
        self.top_p = 1.0
        self.n = 1
        self.max_tokens = 1000
        # todo: logprobs, logitbias, tools, stream, stop
        self.messages = []
        self.api_key = ''
        self.query = ''
        self.reply = ''
        self.response = None

    def set_chat(self):
        """Formats the system prompt into a JSON object for the GPT API"""
        self.messages = [{"role": "system", "content": self.system_prompt}]
        return

    def call_and_response(self):
        """Perform a GPT chat completion: Update the class values for reply and response, and append new messages,
        both user and assistant, to the list-type messages class variable"""
        try:
            self.chat_completion()
            self.reply = self.response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": self.reply})
            print(f"\n{self.reply}\n")
            self.log_conversation()
            self.query = ''
        except Exception as e:
            print(f'[*] error communicating with GPT: {e}')

    def chat_completion(self):
        """Function to perform GPT chat completions via the API"""
        self.messages.append({"role": "user", "content": self.query})
        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            top_p=self.top_p,
            n=self.n,
            max_tokens=self.max_tokens,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        )


class PocketAI(ChatGPT):
    """ChatGPT child class that manages all the aspects of runtime and state"""
    def __init__(self, args):
        super().__init__()
        self.user_input = ''
        self.system_prompt_name = ''
        self.system_prompt = ''
        self.log_file = ''
        self.save_file = ''
        self.log_number = 0
        self.save_number = 1
        self.args = args
        self.freeze = False
        self.log_format = args.log_format  # default='json', options: ['json', 'txt', 'md'], to learn more=README.md
        self.log_level = args.log_level  # default=2, options=[{1: response}, {2:  messages}, {3: response}]
        self.working_dir = get_prog_wd()
        self.config_file = f'{self.working_dir}/config.json'
        self.prompts_dir = f'{self.working_dir}/prompts'
        self.logs_dir = f'{self.working_dir}/logs'

    # Initialization methods & startup checks:

    def init_runtime_checks(self):
        """Performs a series of checks at runtime to make sure the program will operate properly"""
        try:
            exists_or_mkdir(self.logs_dir)
            self.__init__config_json()
            self.log_gen_new()
            self.__api_key_fetch()
            self.gpt_set_params()
            self.__gpt_print_runtime_vars()
            self.__system_prompt_check_args()
            print('[*] startup checks passed')
        except BaseExceptionGroup as e:
            print('[*] initialization error: {e}\n[*] exiting')
            sys.exit()

    def __init__config_json(self):
        """Checks to see if confi.json exists, or generates a new file"""
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                json.dump(variables.config_json_init, f, indent=6)
        else:
            pass

    def log_gen_new(self):
        """Manages log generation"""
        self.__log_number_fetch()
        self.__log_init()

    def __log_init(self):
        """Generates a new logfile relative the current log number"""
        while True:  # to prevent inadvertently overwriting logs if the value is changed in config.json
            self.log_file = f'./logs/log{self.log_number}.{self.log_format}'
            try:
                with open(self.log_file, 'x'):
                    print(f'[*] logfile generated ~ {self.log_file}')
                break
            except FileExistsError:
                self.log_number += 1

    def __log_number_fetch(self):
        """Fetch the log number from config.json and update it"""
        config_data = json_load(self.config_file)
        self.log_number = config_data['log_number']
        config_data['log_number'] = self.log_number + 1
        json_dump(config_data, self.config_file)
        return

    def __api_key_fetch(self):
        """Checks config.json for a stored API key, or prompts the user to input a new key"""
        config_data = json_load('./config.json')
        self.api_key = config_data['api_key']
        if self.api_key:
            good_key = self.api_key_check_valid(self.api_key)
            if good_key:
                return
            else:
                self.api_key_set()
        else:
            self.api_key_set()

    def api_key_check_valid(self, api_key):
        """Send a test message to the GPT API to check if an API key is valid"""
        client = openai.OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                max_tokens=5,
                messages=[{'role': 'user', 'content': 'This is a test .'}])
            self.client = client
        except openai.AuthenticationError:
            print('[*] error, invalid API key')
            self.api_key_set()
        else:
            print('[*] API key verified')
            return True

    def api_key_set(self):
        """Set a new API key and test if it is valid"""
        while True:
            apikey = input('[*] insert OpenAI API key:\n>')
            valid_key = self.api_key_check_valid(apikey)
            if valid_key:
                config_data = json_load('./config.json')
                config_data['api_key'] = apikey
                json_dump(config_data, './config.json')
                self.client = openai.OpenAI(api_key=apikey)
                return
            else:
                pass
# MODEL STATE CONTROLLER
    def gpt_set_params(self):
        """Set the user input runtime parameters for the GPT API, and confirm that they are
        withing acceptable parameters. The functions employed within gpt_set_params verify
        that any user input values fall within an acceptable range, or sets them to their default."""
        self.__gpt_set_model(self.args.model)
        self.__gpt_set_temp(self.args.temperature)  # default=0.7, range(0, 2.0)
        self.__gpt_set_n(self.args.n)  # default=0, range=(-2.0, 2.0)
        self.__gpt_set_fp(self.args.frequency_penalty)  # default=0, range=(-2.0, 2.0)
        self.__gpt_set_pp(self.args.presence_penalty)  # default=1.0, range=(0, 1.0)
        self.__gpt_set_tp(self.args.top_p)  # default=1, range=(0.1, 1)
        self.__gpt_set_mt(self.args.max_tokens)  # default=1000, max relative to GPT model, but typically 4096
        self.__gpt_set_ll(self.args.log_level)  # default=2, range=(1, 2)
        self.__gpt_set_lf(self.args.log_format)  # default='json', options=['json', 'txt']
        # todo: self.stop_sequence = args.stop  # default: None
        # todo: self.stream = args.args.stream
        # todo: self.logit_bias = args.logit_bias
        # todo: self.tools = args.tools # currently out of scope

    def __gpt_set_model(self, new_value):
        for model in variables.models:
            if model == new_value:
                self.model = new_value
                return
        self.__gpt_runtime_error(variables.bad_model, new_value)
        self.model = ChatGPT().model

    def __gpt_set_temp(self, new_value):
        if 0.0 <= new_value <= 2.0:
            self.temperature = new_value
        else:
            self.__gpt_runtime_error(variables.bad_temp, new_value)
            self.temperature = ChatGPT().temperature

    def __gpt_set_fp(self, new_value):
        if -2.0 <= new_value <= 2.0:
            self.frequency_penalty = new_value
        else:
            self.__gpt_runtime_error(variables.bad_fp, new_value)
            self.frequency_penalty = ChatGPT().frequency_penalty

    def __gpt_set_pp(self, new_value):
        if -2.0 <= new_value <= 2.0:
            self.presence_penalty = new_value
        else:
            self.__gpt_runtime_error(variables.bad_pp, new_value)
            self.presence_penalty = ChatGPT().presence_penalty

    def __gpt_set_tp(self, new_value):
        if 0 <= new_value <= 1.0:
            self.top_p = new_value
        else:
            self.__gpt_runtime_error(variables.bad_tp, new_value)
            self.top_p = ChatGPT().top_p

    def __gpt_set_n(self, new_value):
        if 1 <= new_value <= 20:
            self.n = new_value
        else:
            self.__gpt_runtime_error(variables.bad_n, new_value)
            self.n = ChatGPT().n

    def __gpt_set_mt(self, new_value):
        if 1 <= new_value <= 4096:
            self.max_tokens = new_value
        else:
            self.__gpt_runtime_error(variables.mt, new_value)
            self.max_tokens = ChatGPT().max_tokens

    def __gpt_set_ll(self, new_value):
        if 1 <= new_value <= 2:
            self.log_level = new_value
        else:
            self. __gpt_runtime_error(variables.bad_ll, self.log_level)
            self.log_level = 2

    def __gpt_set_lf(self, new_value):
        if new_value == 'txt' or new_value == 'json':
            self.log_format = new_value
        else:
            self.__gpt_runtime_error(variables.bad_lf, self.log_format)
            self.log_format = 'json'

    @staticmethod
    def __gpt_runtime_error(reason, cause):
        """Neatly prints an error message for the preceding functions - see variables.py for error messages"""
        print(reason.format(cause))
        print('[*] resetting value to default')

    def __gpt_print_runtime_vars(self):
        """Prints a few basic GPT API parameters, as well as any parameter that differs from the default"""
        current_vars = vars(self)
        parent_vars = vars(ChatGPT())
        print("\n[*] GPT parameters:")
        for k in current_vars.keys():
            if k in parent_vars and k != 'client' and current_vars[k] != parent_vars[k] \
                    or k in variables.startup_params:
                print(f'[-] {k}: {current_vars[k]}')
        print()

    # System prompt methods:

    def system_prompt_set(self):
        if not self.system_prompt:
            self.system_prompt = input("\n[*] Input a system prompt, or hit enter to view preexisting options:\n>")
            if self.system_prompt:
                self.system_prompt_name = 'custom'
                print('\n[*] query AI:')
                return
            while self.system_prompt == '':
                category = self.__system_prompt_select_category()
                users_choice = self.__system_prompt_select_prompt(category)
                self.system_prompt_name = users_choice
                if users_choice == 'back':
                    pass
                else:
                    path_sys_prompt = f'{get_prog_wd()}/prompts/{category}/{users_choice}'
                    prompt = fetch_contents(path_sys_prompt)
                    print(f'\n{prompt}\n')
                    set_prompt = input("[*] Select prompt, 'enter' or 'n'?\n>")
                    if set_prompt != 'n':
                        self.system_prompt = prompt
        print(f"\n[*] System prompt: {self.system_prompt_name}\n[*] query AI:\n")

    def __system_prompt_select_category(self):
        """Select a system prompt category from the pre-made options"""
        print('\n[-] Categories\n')
        prompts_dir = f'{self.working_dir}/prompts'
        categories = fetch_from(prompts_dir)
        categories.sort()
        choice = self.make_choice(categories)
        print(f'\n[*] Category: {choice}')
        return choice

    def __system_prompt_select_prompt(self, category):
        """Select a pre-made system prompt from a particular category"""
        print('[-] Prompts\n')
        category = f'{self.working_dir}/prompts/{category}'
        sys_prompts = fetch_from(category)
        sys_prompts.sort()
        return self.make_choice(sys_prompts, go_back=True)

    def __system_prompt_check_args(self):
        """Check to see if the user supplied the path to a system prompt at runtime"""
        if self.args.system_prompt:
            self.system_prompt_name = self.args.system_prompt.rpartition('/')[-1]
            self.system_prompt = fetch_contents(self.args.system_prompt)

    @staticmethod
    def enumerate_list(options_list, go_back=False):
        """"Enumerates a list of options"""
        for x, _item in enumerate(options_list, 1):
            print(f'{x}. {_item}')
        if go_back:
            print(f'{x + 1}. back')
        return

    def make_choice(self, options_list, go_back=False):
        """Select from a list of options by the objects enumerated position"""
        while True:
            self.enumerate_list(options_list, go_back)
            selection = input('\n[*] Selection by position:\n>')
            try:
                selection = int(selection)
                if 1 <= selection <= len(options_list):
                    return options_list[selection - 1]
                elif go_back and selection == len(options_list) + 1:
                    return 'back'
                else:
                    raise ValueError
            except ValueError:
                print('[*] Invalid selection')

    # Primary program loop:

    def chat_with_gpt(self):
        """Initialize a conversation with GPT until the user resets the chat or the token limit is reached"""
        while True:
            try:
                self.get_input()
                self.call_and_response()
            except Exception as e:
                print(f'[*] error: {e}')

    # Input & parsing

    def get_input(self):
        """Implements a finite state machine, via parsing user input, to manipulate the program during runtime"""
        while True:
            self.user_input = input('>') # INSTEAD OF MAKING A MEMBER MAKE IT A PARAMETER
            if self.user_input.startswith('>'):
                self.__cmd_parse()
            elif not self.freeze:
                if self.query:
                    print(self.query)  # testing
                    return
                else:
                    self.query = self.user_input
                    return
            elif self.freeze:
                self.query += f'\n{self.user_input}'

    def __cmd_parse(self):
        """Parse input for runtime commands, and if command execute a specific function"""
        try:
            if self.user_input == ">" or self.user_input == '>help':
                self.__cmd_help()
            elif self.user_input.startswith('>stop'):
                self.freeze = True
            elif self.user_input.startswith('>start'):
                self.freeze = False
            elif self.user_input.startswith('>exec'):
                self.__cmd_exec()
            elif self.user_input.startswith('>insert'):
                self.__cmd_insert()
            elif self.user_input.startswith('>reset'):
                self.__cmd_reset()
            elif self.user_input.startswith('>show'):
                self.__cmd_show()
            elif self.user_input.startswith('>flush'):
                self.query = ''
            elif self.user_input.startswith('>save'):
                self.__cmd_save()
            elif self.user_input.startswith('>set'):
                self.__cmd_set()
            elif self.user_input.startswith('>exit'):
                print("[*] exiting")
                sys.exit()
            self.user_input = ''
        except Exception as e:
            print(f'[*] error: {e}')

    # Context management commands:

    # >
    @staticmethod
    def __cmd_help():
        """Prints the help string for the runtime commands"""
        print(variables.HKR)
        print(variables.state_commands_help)

    # >exec
    def __cmd_exec(self):
        """Execute a system-wide command from within the program"""
        cmds = self.user_input.split(' ')
        if cmds[1] == 'cd':  # hack to allow the user to change directories
            try:
                if cmds[2] == 'home':
                    os.chdir(self.working_dir)
                else:
                    os.chdir(cmds[2])
            except Exception as e:
                print(f'[*] error: {e}')
        elif cmds[1] == 'cat':
            contents = fetch_contents(cmds[2])
            print(contents, '\n')
        else:
            output = subprocess.check_output(cmds[1], shell=True, text=True, stderr=subprocess.STDOUT, timeout=3)
            print(output)

    # >show
    def __cmd_show(self):
        """Print user selected runtime variables to the console"""
        if ' ' in self.user_input:
            arguments = self.user_input.split(' ')
            if arguments[1] == 'tokens':
                print(f'[*] Tokens used: {response["usage"]["prompt_tokens"]}')
            elif arguments[1] == 'gpt':
                self.__show_vars_gpt()
            elif arguments[1] == 'vars':
                self.__show_vars()
            else:
                self.__show_var()
        else:
            print(f'\n```query\n{self.query}```')

    def __show_var(self):
        """Print the value for a single ChatGPT API variable"""
        current_parameters = vars(self)
        for k in current_parameters.keys():
            if k == self.user_input.split(' ')[1]:
                print(f'[-] {k}: {current_parameters[k]}\n')

    def __show_vars(self):
        """Print all the current parameters for the ChatGPT API"""
        print("\n[*] GPT parameters:")
        self.__show_pretty_print(variables.vars_gpt)
        print("\n[*] runtime variables:")
        self.__show_pretty_print(variables.vars_runtime)
        print(f"\n[*] directory info")
        self.__show_pretty_print(variables.vars_directory)

    def __show_vars_gpt(self):
        print('\n[*] GPT parameters:')
        self.__show_pretty_print(variables.vars_gpt)

    def __show_pretty_print(self, select_vars):
        current_vars = vars(self)
        for k in current_vars.keys():
            if k in select_vars:
                print(f"[-] {k}: {current_vars[k]}")

    # >reset
    def __cmd_reset(self):
        """Initialize a new chat session, by resetting the system prompt."""
        if self.user_input.startswith('>reset'):
            self.user_input = ''
            self.query = ''
            self.system_prompt = ''
            self.messages = []
            self.log_gen_new()
            self.system_prompt_set()
            self.set_chat()

    # >insert
    def __cmd_insert(self):
        """If sending messages to GPT is frozen (freeze=True), append the contents of a file to the query"""
        if self.freeze and ' ' in self.user_input:
            arguments = self.user_input.split(' ')
            insert_me = fetch_contents(arguments[1])
            self.query += f'{self.query}\n{insert_me}'
        else:
            print('[*] invalid command')

    # >save
    def __cmd_save(self):
        if ' ' in self.user_input:
            arguments = self.user_input.split(' ')
            if len(arguments) != 3:
                self.__save_update_savefile()
            else:
                self.save_file = arguments[2]
            if arguments[1] == 'code':
                self.__save_code(arguments)
            elif arguments[1] == 'reply':
                self.__save_reply(arguments)
            elif arguments[1] == 'response':
                self.__save_response(arguments)

    def __save_code(self, arguments):
        p = re.compile("```((.|\n)*)```")
        match = re.search(p, self.reply)
        if match:
            save_text(self.save_file, match.group())
            print(f'[*] saving code to ~ {self.save_file}')

    def __save_reply(self, arguments):
        save_text(self.save_file, self.reply)
        print(f'[*] saving reply to ~ {self.save_file}')

    def __save_response(self, arguments):
        save_text(self.save_file, str(self.response))
        print(f'[*] saving response to ~ {self.save_file}')

    def __save_update_savefile(self):
        self.save_file = f'{os.getcwd()}/log{self.log_number}-{self.save_number}.pktai'
        self.save_number += 1

    def __cmd_set(self):
        if ' ' in self.user_input:
            arguments = self.user_input.split(' ')
            try:
                if arguments[1] == 'model':
                    self.__gpt_set_model(arguments[2])
                elif arguments[1] == 'temperature':
                    value = float(arguments[2])
                    self.__gpt_set_temp(value)
                elif arguments[1] == 'top_p':
                    value = float(arguments[2])
                    self.__gpt_set_tp(value)
                elif arguments[1] == 'frequency_penalty':
                    value = float(arguments[2])
                    self.__gpt_set_fp(value)
                elif arguments[1] == 'presence_penalty':
                    value = float(arguments[2])
                    self.__gpt_set_pp(value)
                elif arguments[1] == 'max_tokens':
                    value = int(arguments[2])
                    self.__gpt_set_mt(value)
                elif arguments[1] == 'n':
                    value = int(arguments[2])
                    self.__gpt_set_n(value)
                else:
                    raise TypeError
                print(f'[-] {arguments[1]}: {self.temperature}\n')
            except TypeError:
                print(f'[*] invalid type or value for {arguments[1]}\n[-] resetting to default')

    # logging:

    def log_conversation(self):
        """Logs the response or messages as a JSON or TXT file relative to the user's runtime settings"""
        try:
            if self.log_level == 1 and self.log_format == 'json':
                print('[*] log_level 1 only supports .txt output')
                self.log_format = 'txt'
            if self.log_level == 1:
                json_dump(str(self.response), self.log_file)
            elif self.log_level == 2 and self.log_format == 'json':
                json_dump(self.messages, self.log_file)
            elif self.log_level == 2 and self.log_format == 'txt':
                with open(self.log_file, 'w') as f:
                    for i in range(len(self.messages)):
                        f.write(f"{self.messages[i]['role']}:--------------\n\n{self.messages[i]['content']}\n\n")
        except ExceptionGroup as e:
            print(f'[*] logging error: {e}')


# portable utility functions:


def exists_or_mkdir(directory):
    """Checks if a directory exists or creates it"""
    path = pathlib.Path(directory)
    path.mkdir(exist_ok=True)
    return


def json_load(json_file):
    """Loads JSON object from a file"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def json_dump(json_dict, json_file):
    """Dumps a JSON object to a file"""
    with open(json_file, 'w') as f:
        json.dump(json_dict, f, indent=6)


def save_text(filename, _text):
    """Simple funtion to save text to a file"""
    with open(filename, 'w') as f:
        f.write(_text)


def fetch_contents(file_path):
    """Returns the contents of a file as a string type variable"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        pass


def get_prog_path():
    """Returns the program's path"""
    prog_path = os.path.abspath(__file__)
    return prog_path


def get_prog_wd():
    """Returns the current program's working directory"""
    prog_path = get_prog_path()
    root_dir = os.path.dirname(prog_path)
    return root_dir


def fetch_from(root_dir):
    """Returns a list containing the contents of a directory"""
    directories = os.listdir(root_dir)
    return directories


def args_fetch():
    p = argparse.ArgumentParser(description=variables.pocket_ai)
    p.add_argument('-sp', '--system-prompt', required=False, default=None, dest='system_prompt',
                   help=variables.system_prompt),
    p.add_argument('-m', '--model', default='gpt-3.5-turbo', type=str, choices=variables.models,
                   help=variables.model),
    p.add_argument('-t', '--temperature', type=float, default=0.7,  # min=0, max=2.0,
                   help=variables.temperature),
    p.add_argument('-fp', '--frequency-penalty', type=float, default=0,  # min=-2.0, max=2.0,
                   help=variables.frequency_penalty),
    p.add_argument('-pp', '--presence-penalty', type=float, default=0,  # min=-2.0, max=2.0,
                   help=variables.presence_penalty),
    p.add_argument('-tp', '--top-p', type=float, default=1.0, help=variables.top_p),  # min=0.1, max=1.0,
    p.add_argument('-st', '--stop', default=[], nargs='*', help=variables.stop),
    p.add_argument('-mt', '--max-tokens', type=int, default=1000, help=variables.max_tokens),
    p.add_argument('-n', type=int, default=1, help=variables.n),
    p.add_argument('--log-level', '-ll', default=2, type=int, help=variables.log_level),
    p.add_argument('-lf', '--log-format', default='json', type=str, help=variables.log_format)
    return p.parse_args()


if __name__ == '__main__':
    try:
        print(variables.HKR)
        parser = args_fetch()
        pocketai = PocketAI(parser)
        pocketai.init_runtime_checks()
        pocketai.system_prompt_set()
        pocketai.set_chat()
        pocketai.chat_with_gpt()
    except KeyboardInterrupt:
        print("\n[*] exiting\n")
