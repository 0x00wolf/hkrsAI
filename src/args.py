import argparse
from src.argshelp import *


def fetch_args():
    """Function to handle command-line arguments"""
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog='hkrsAI.v2',
        description=DESCRIPTION,
        epilog=MORE_INFO
    )
    p.add_argument('--system-prompt', '-sp', required=False, default=None, dest='system_prompt',
                   help=SYSTEM_PROMPT),
    p.add_argument('--model', '-m', default='gpt-3.5-turbo', type=str, choices=['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo'],
                   help=MODEL),
    p.add_argument('--temperature', '-t', type=float, default=0.7,  # min=0, max=2.0,
                   help=TEMPERATURE),
    p.add_argument('--frequency-penalty', '-fp', type=float, default=0,  # min=-2.0, max=2.0,
                   help=FREQUENCY_PENALTY),
    p.add_argument('--presence-penalty', '-pp', type=float, default=0,  # min=-2.0, max=2.0,
                   help=PRESENCE_PENALTY),
    p.add_argument('--top-p', type=float, default=1.0, help=TOP_P),  # min=0.1, max=1.0,
    # todo: p.add_argument('-st', '--stop', default=[], nargs='*', help=variables.stop),
    p.add_argument('--max-tokens', '-mt', type=int, default=1000, help=MAX_TOKENS),
    p.add_argument('-n', type=int, default=1, help=N),
    p.add_argument('--log-level', '-ll', default=2, type=int, help=LOG_LEVEL),
    p.add_argument('--log-format', '-lf', default='json', type=str, help=LOG_FORMAT)
    return p.parse_args()

