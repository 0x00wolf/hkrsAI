import dataclasses
from src.action import Action


COMMANDS = ['stop', 'start', 'insert', 'flush', 'exec', 'set', 'reset', 'show', 'save', 'help', 'exit']


class InputParser:
    @staticmethod
    def parse(user_input):
        """parses user input and passes an Action to the Dispatcher"""
        if user_input.startswith('>'):
            if ' ' in user_input:
                user_input = user_input.split(' ')
                command = user_input.pop(0).replace('>', '')
                arguments = user_input[:]
                return Action(command=command, arguments=arguments)
            else:
                command = user_input.replace('>', '')
                for _command in COMMANDS:
                    if command == _command:
                        return Action(command=command)
                return Action(command='error')
        else:
            action = Action(command='chat', raw_input=user_input)
            return action

