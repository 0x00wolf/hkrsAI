import sys
from args import fetch_args
from pathfinder import PathFinder
from client import Client
from gpt import GPT
from systemprompt import SystemPrompt
from conversation import Conversation
from action import Action
from inputparser import InputParser
from dispatcher import Dispatcher
from logger import Logger
import readline


HKRSAI = """
1  0  1
1  1  0
0  0  0
hkrsAI.v2
"""


def main():
    print(HKRSAI)
    args = fetch_args()  # command-line arguments
    paths = PathFinder()  # necessary paths for runtime

    client = Client(config=paths.config)  # OpenAI API client management object
    client.initialize()  # Checks for valid saved API key or prompts user. Tests keys before proceeding
    gpt = GPT(  # Class that contains GPTs parameters
        client=client.client,
        model=args.model,
        temperature=args.temperature,
        top_p=args.top_p,
        n=args.n,
        frequency_penalty=args.frequency_penalty,
        presence_penalty=args.presence_penalty,
        max_tokens=args.max_tokens
    )
    parser = InputParser()  # Class to parse user input and return Actions.
    dispatcher = Dispatcher()  # Manages conversation state and turnsActions into functions.
    logger = Logger(paths=paths, log_level=args.log_level, log_format=args.log_format)

    system_prompt = SystemPrompt(prompts_dir=paths.prompts, path=args.system_prompt)
    conversation = Conversation().start(system_prompt.content)  # program manages a conversation

    while True:
        user_input = input('>')  # While True, take user input
        action = parser.parse(user_input)  # Parser turns input into an Action.
        function = dispatcher.dispatch(action)  # Dispatcher turns Actions into functions with the same signature
        gpt, conversation, logger = function(gpt, conversation, action=action, logger=logger)  # This is a Conversation


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[*] exiting\n')
        sys.exit()
