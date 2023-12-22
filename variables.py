HKR = """
1 0 1
1 1 0
0 0 0

[*] pocketAI"""

pocket_ai = """PocketAI is a ligalternative to proprietary terminal wrappers for Phtweight wrapper for OpenAI API for GPT chat completions.\
For detailed information on usage see the README.md."""

state_commands_help = """
[*] State commands: 
- all commands must be prepended with '>'

---

[*] command:\t>'  or ' >help'  
[-] info:
-Displays this message.

----

[*] command:\t'>stop'
[*] usage: >">stop"
[-] info:
- Sets the pocketAI class variable freeze to True, allowing for copying and pasting to the terminal.
- Allows the user to build a query from a series of inputs, with each input parsed for state commands.
- Users can insert the contents of a file into their query, while freeze=True with the '>insert' command (see below).
[-] example:
stop

----

[*] command:\t'>start'  
[*] usage: >">start"
[-] info:
- Sets freeze to False. 
- Hit enter when the prompt returns to submit the query to the GPT API.
- Note that some commands only work when freeze is True.
[-] example:
>start

----

[*] command:\t'>exec'  
[-] usage: >">exec {system_command} {args[1:]}"
[-] info:
- Allows the user to execute system commands within pocketAI's shell.
- Any additional arguments in the input will be executed as a system commands.
- Note that the program runs in a Python shell, which technically doesn't have access to the 'cd' command,
but 'cd' has been included thanks to a little hack.
- The primary function of being able to execute system commands is directory traversal and organizing files.
[-]examples:
>exec cd ./path  
>exec cd /root/path'       
>exec cd home  # jumps to pocketAI's root directory.          
>exec ls -l
>exec mkdir ./dir_name 

----

[*] command:\t'>stop'  
[*] usage: >">stop"
[-] info:
- Sets the pocketAI class variable freeze to True, allowing for copying and pasting to the terminal
- Allows the user to build a query from a series of inputs, with each input parsed for state commands
- Users can insert the contents of a file into their query, while freeze=True with the '>insert' command (see below)

----

[*] command:\t>insert'  
[*] usage: >">insert  /path/to/file.extension"
[-] info:
- Fetches the contents of a file and appends it to the query.
- Requires freeze=True.
[-] example:
>insert /home/user/Projects/CurrentProject/what_im_working_on.py
>insert ./code_for_query.c

----

[*] command:\t'>reset'             
[*] usage: >">reset"       
[-] info:
- Resets the system prompt, generates a new log, and initiates a new chat session.
- Note: This command will clear the current query, and messages. Before a new command is sent to the GPT
API the user is still able to save the previous response, which will be replaced with the response from the API.

----

[*] command:\t'>show' or 'print''  
[*] usage: >">show ( 'query' | 'response' | 'tokens' | 'system' | 'vars' | 'var {GPT parameter}')"
[-] info:
- By default, inputting '>show' or '>print' will print the contents of the current query saved in memory. 
- By adding an additional arguments, pocketAI will display the values pertaining to that value.
- 'vars' prints all of the set values for ChatGPT's parameters.
- 'var' displays a specific parameter, which the user must specify.
[-] examples:
>show tokens                        # display the number of tokens expended
>show var top_n                   # display the current temperature setting
>show system                       # display the system prompt

----

[*] command:\t'>flush' 
[*] usage: >">flush"                    
[-] info:
- Resets the query to ''.

----

[*] command:\t'>save'  
[*] usage: >">save  ('code' | 'response' | 'reply' | 'messages')  /output_path/filename"                        
[-] info:
- Allows the user to save the current response, messages, last reply, or extract and save code from the last reply.
- The reply and messages can be saved in either human readable text, or formatted JSON output. 
- To select a format, append the appropriate suffix to the file path argument.
[-] examples:
save code ./file_in_current_dir.py
save code /absolute/path/to/file.js
save reply ./dns_tunnelling.txt

----

[*] command:\t'>exit'
[*] usage: >">exit"                     
[-] info:
- Quit the program.
"""


# Definitions of Chat GPT tweaks  courtesy of:
# https://platform.openai.com/docs/api-reference/chat/create

# To add new prompts simply add the file into one of the subdirectories in ./prompts
system_prompt = """Optional: Specify the path to a system prompt at runtime. The system prompt \
can be used to specify the persona used by the model in its replies."""

temperature = """What sampling temperature to use, between 0 and 2. Higher values like 0.8 will \
make the output more random, while lower values like 0.2 will make it more focused \
and deterministic. We generally recommend altering this or top_p but not both."""

top_p = """An alternative to sampling with temperature, called nucleus sampling, \
where the model considers the results of the tokens with top_p probability \
mass. So 0.1 means only the tokens comprising the top 10%% probability mass \
are considered. OpenAI generally recommend altering this or temperature but not both."""

frequency_penalty = """Number between -2.0 and 2.0. Positive values penalize \
new tokens based on their existing frequency in the text so far, decreasing the \
model's likelihood to repeat the same line verbatim."""

presence_penalty = """Number between -2.0 and 2.0. Positive values penalize new \
tokens based on whether they appear in the text so far, increasing the model's likelihood \
to talk about new topics. For more information please visit: \
https://platform.openai.com/docs/guides/text-generation/parameter-details"""

logit_bias = """""Modify the likelihood of specified tokens appearing in the completion. \
Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) \
to an associated bias value from -100 to 100. Mathematically, the bias is added to the \
logits generated by the model prior to sampling. The exact effect will vary per model, \
but values between -1 and 1 should decrease or increase likelihood of selection; values \
like -100 or 100 should result in a ban or exclusive selection of the relevant token."""

max_tokens = """The maximum number of tokens to generate in the chat completion.  \
The total length of input tokens and generated tokens is limited by the model's \
context length."""

n = """How many chat completion choices to generate for each input \
message. Note that you will be charged based on the number of generated \
tokens across all of the choices. Keep n as 1 to minimize costs. By default \
pocketAI limits the max value of n to 20. To change this edit the code in the pocketAI \
class"""

model = """The OpenAI API is powered by a diverse set of models with different \
capabilities. To learn more go to: https://platform.openai.com/docs/models/overview"""

models = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo']

stop = """Up to 4 sequences where the API will stop generating further tokens."""

# Printouts if GPT parameters are outside their accepted type or range

bad_model = "[*] invalid option: if you are confident the model you are attempting to use is valid" \
            "please add it to the list in variables.py in the program's parent directory.\n"

bad_temp = '[*] invalid temperature: {}\n[*] type=float, valid_range=(0, 2.0), default=0.7\n'

bad_pp = '[*] invalid presence_penalty: {}\n[*] type=float, valid_range=(-2.0, 2.0), default=0]\n'
bad_fp = '[*] invalid frequency_penalty: {}\n[*] valid_range=(-2.0, 2.0), default=0\n'

bad_tp = '[*] invalid top_p: {}\n[*] type=float, valid_range=(0, 1.0), default=1.0\n'

bad_n = '[*] invalid n: {}\n[*] type=int, valid_range=(1, 20), default=1.0\n'

bad_ll = '[*] invalid log_level: {}\n[*] type=int, valid_range(1,2), default=2\n'

bad_lf = "[*] invalid log_format: {}\n[*] type=str, options=['json', 'txt']\n"

config_json_init = {'log_number': 0, 'api_key': ''}

startup_params = ['model', 'temperature', 'top_p']

linux_abs_or_rel_file = r"^(<paste ')(\.?/?[A-Za-z0-9]+_*-*)*(.)([A-Za-z0-9]+)('>)"

float_params = ['temperature', 'top_p', 'frequency_penalty', 'presence_penalty']

int_params = ['max_tokens', 'n']

vars_gpt = ['model', 'temperature', 'top_p', 'n', 'frequency_penalty', 'presence_penalty', 'max_tokens']

vars_runtime = ['freeze', 'log_level', 'log_format']

vars_directory = ['log_file', 'working_dir']

log_level = """Accepts a number, either 1 or 2.  Default logging level is 2.
Log level 1 saves the entire response from the API. 
Log level 2 only saves the user and assistant messages."""

log_format = """Accepts a string, either 'json' or 'txt'. Json is set by default. 
Txt is only available for log-level 2 messages and reply's from GPT, and 
will automatically reset to json if the user selects both txt and log level 1."""

defaults = {'model': 'gpt-3.5-turbo', 'temperature': 0.7, 'top_p': 1, 'frequency_penalty': 0, 'presence_penalty': 0, 'n': 1, 'max_tokens': 1000 }