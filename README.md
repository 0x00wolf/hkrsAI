

<!-- ABOUT THE PROJECT -->
## hkrAI - the keep it simple approach to integrating the world's most power AI into your Linux terminal.

There are a lot of options for propeitary software to take advantage of integrating ChatGPT into your workflow, most of them include telemetry and are GUI based. In the principle of KISS (not the band), I wanted a tool that integrated seamlessly into my development workflow, but streamlined enough to fit nicely into a single Python file (with a second to contain long string variables). I wanted to be able to copy+paste, insert files with a single command, execute system wide commands for directory traversal, have automatic logging in case I wanted to come back to something, but didn't remember to save it, and the ability to extract code easily. After 8 solid days of coding, I ended up with a program that integrated all the features that I wanted: hkrAI!

hkrAI is modeled as a finite state machine, allowing you to perpetually engage in conversations with custom AI's for any circumstance. The program includes 100's of premade system prompts from the most popular repos on Github (AwesomeChatGPTFonts), which can be selected via a convenient menu system at anytime within the program.

I built hkrAI as a daily use productivity tool for myself, and I absolutely love it. I hope you will too!

All of the program's logic is in one file, with as logical and clean code as I can muster. If you want to edit any features, please fork the project or reach out to me with your ideas.

<!-- GETTING STARTED -->
### Getting started:

hkrAI uses one non-standard Python Library, the OpenAI lib: [https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)

**Steps to install:**

1. Get an API Key at [https://example.com](https://platform.openai.com/signup)](https://platform.openai.com/signup)
2. Clone the repo
   ```sh
   git clone https://github.com/0x00wolf
   ```
3. Install the OpenAI Python library (I suggest using a venv);
   ```python
   pip install openai
   ```
4. Run the program
   ```Python
   ./hkrai.py 
   ```
5. Input your API when prompted.
6. Select a premad system prompt or input your own.
7. Once a system prompt has been entered, input '>' to view the context management commands manual (or see below).
---
### First Runtime

The first time you run hkrAI it will generate JSON config file in the parent directory. The config file tracks log numbers, and stores the user's API key for communicating with ChatGPT. By default, hkrAI will check for a key and prompt you to insert one if none is present. The program also verifies the validity of keys at boot up, or anyitme you initate a new chat session.

Logfiles will be saved in the logs folder in the parent directory. This will also be generated on the first runtime.

---
### Command Line Arguments

The command line arguments include each of the GPT API's parameters, as well as logging-level, log format, and system prompt.

To view detailed information about hkrAI's runtime parameters in the terminal, you can input:

```python
./hkrai.py -h
```

Although you can find detailed information in the help strings on each of the parameters and their functions, explaining their individual use case is beyond the scope of this README.md. Please see: [OpenAI's Docs](https://openai.com
_For more examples, please refer to the [OpenAI API Documentation](https://platform.openai.com/docs/api-referen)

Example runtime arguments:

```bash
./hkrai.py -sp ./prompts/fun/yoda --temperature 1.2 --max-tokens 200 --log-format txt
```
---
### Context Management Commands

**>stop**
[*] usage: 

```
>stop
```
info:
  - Sets the pocketAI class variable freeze to True, allowing for copying and pasting to the terminal.
  - Allows the user to build a query from a series of inputs, with each input parsed for state commands.
  - Users can insert the contents of a file into their query, while freeze=True with the '>insert' command (see below).
---

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
<!-- ROADMAP -->
## Roadmap

- [x] Beta release
- [ ] Beta tester bug hunt *in progress
- [ ] Add Additional features and integration based on user feedback

## Contact

Wolf - 0x00w0lf@proton.me
Project Link: [https://github.com/0x00wolf/hkrai](https://github.com/0x00wolf/hkrai)
