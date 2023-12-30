HELP_STRING = """----------------------------------------------
command: >stop

info: Sets thinking=True, halting messages being sent to GPT. While thinking=True, \
new inputs are appended to the query with a '\n', allowing the user to create a stacked query \
from X inputs. While thinking=True, the user is able to copy+paste to the program's Python \
shell, as well as use the '>insert' command (see below).
----------------------------------------------
command: >flush

info: While thinking=True, clears the value stored in the query. Aka, the fat fingers insurance \
clause.
----------------------------------------------
command: >insert

>insert /absolute/path/filename.extension
>insert ./relative/path/filename.extension

info: When thinking=True, '>insert' fetches the contents of a file and appends it to the query. \
Primarily a feature for developers to easily import code from their projects into the program, \
or to enable more advanced scripting capabilities.
----------------------------------------------
command: >start

info: Set thinking=False. The next input will trigger sending the stored query to GPT, \
resuming the conversation.
----------------------------------------------
command: >exec

>exec {system command} {args}
>exec cd ./logs  # cd to relative or absolute file path
>exec cd home  # returns to the hkrsAI parent directory
>exec ls -l
>exec cat ./filepath/filename.extension     # fetches and prints the contents of a file

info: You can execute system-wide commands from within the program's Python shell. Note that \
'cd', and 'cat' are hacked in. Many Linux programs will fail to execute. Primarily included to enable \
easy directory traversal for workflow integration.
----------------------------------------------
command: >save

>save  # saves the AIs last reply to a generic save file
>save /path/filename.extension  # saves the AIs last reply to relative or absolute path
>save code  # extracts code from the last reply and saves it to a generic save file
>save code ./path/filename.extension  # extracts and saves code to a relative or absolute path
>save reply {None | /path/filename.extension}
>save response {None | /path/filename.extension}
>save messages {None | /path/filename.extension}

info: Allows the user to extract and save code or text to relative, absolute, or generic file path.
----------------------------------------------
command: >set

>set gpt {parameter} {value}
>set logger {level | format} 
>set {gpt_parameter} {value}  # for more information see ./hkrsai.py -h
>set {level} {value}  # levels: (1, 2)
>set {format} {value}  # format: ['json', 'txt']

info: Changes the value with the associated parameter.
----------------------------------------------
command: >show

>show  # prints the value stored in conversation.query
>show {conversation | gpt | logger } {key}
>show {gpt parameter}  # prints the value for a specific gpt parameter
>show  # prints the values stored in gpt and logger
>show gpt  # prints the values stored in gpt

info: Prints stored values to the console.
----------------------------------------------
command: >reset

>reset  # resets the AI assistant
>reset conversation  # resets the AI assistant
>reset log  # starts a new log file

info: Allows the user to reset the conversation or start a new log.
----------------------------------------------
command: >exit

info: Quit the program.
"""