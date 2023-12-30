import os


class SystemPrompt:
    """A class that manages setting the system prompt used to define AI assistants. \
    To add a new system prompt that will be selectable from the runtime menu, \
    copy the prompt to an extensionless file in the appropriate category folder."""
    def __init__(self, prompts_dir, path=''):
        self.dir = prompts_dir
        self.path = path
        self.content = ''
        self.title = 'custom'
        self._start()

    def _start(self):
        """Allow the user to define a custom prompt, or select one of the pre-made options"""
        if not self.path:
            self.content = input("\n[*] input a custom system prompt, \
                                       \n[*] hit enter to view preexisting options:\n>")
            if not self.content:
                self._set()
        else:
            self.content = self._fetch_contents(self.path)
            self.title = self.path.rpartition('/')[-1]

    def _set(self):
        """Loop that runs until a prompt has been selected"""
        while True:
            category = self._select_category()
            title = self._select_prompt(category)
            if title == 'back':
                pass
            else:
                self.path = f'{self.dir}/{category}/{title}'
                prompt = self._fetch_contents(self.path)
                print(f'\n{prompt}\n')
                set_prompt = input("[*] select prompt\n\n[-] 'enter' to accept\n[-] 'n' to go back\n"
                                   "[-] 'x' to enter a custom font'\n>")
                if set_prompt == 'x':
                    return SystemPrompt(prompts_dir=self.dir)
                elif set_prompt == 'n':
                    pass
                else:
                    self.title = self.path.rpartition('/')[-1]
                    self.content = prompt
                    print(f'[*] system prompt: {self.title}\n[*] query AI:')
                    return

    def _select_category(self):
        """Select a system prompt category from the pre-made options"""
        print('\n[-] categories\n')
        categories = self._fetch_from(self.dir)
        categories.sort()
        choice = self._make_choice(categories)
        print(f'\n[*] category: {choice}')
        return choice

    def _select_prompt(self, category):
        """Select a pre-made system prompt from a particular category"""
        print('[-] prompts\n')
        category = f'{self.dir}/{category}'
        system_prompts = self._fetch_from(category)
        system_prompts.sort()
        self.path = self._make_choice(system_prompts, go_back=True)
        return self.path

    def _make_choice(self, options_list, go_back=False):
        """Provides the user with the ability to select a prompt from an enumerated options list"""
        # Select from a list of options by the objects enumerated position
        while True:
            try:
                self._enumerate_list(options_list, go_back)
                selection = input('\n[*] select by position:\n>')
                selection = int(selection)
                if 1 <= selection <= len(options_list):
                    return options_list[selection - 1]
                elif go_back and selection == len(options_list) + 1:
                    return 'back'
            except ValueError:
                print('[*] invalid selection')

    @staticmethod
    def _enumerate_list(options_list, go_back=False):
        """"Enumerates a list of options"""
        for x, _item in enumerate(options_list, 1):
            print(f'{x}. {_item}')
        if go_back:
            print(f'{x + 1}. back')

    @staticmethod
    def _fetch_contents(file_path):
        """Fetches the contents of a file"""
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            pass

    @staticmethod
    def _fetch_from(root_dir):
        """Returns a list containing the contents of a directory"""
        directories = os.listdir(root_dir)
        return directories

