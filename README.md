<!-- ABOUT THE PROJECT -->

# HkrsAI.v2

---
![alt text](https://github.com/0x00wolf/hkrsAI/blob/main/logo.png)

---

## Description:

   
**Version 2 is out!**

HkrsAI is designed to increase the productivity of programmers and pentestests by integrating ChatGPT into their workflow seamlessly. Features like code extraction, and the ability to insert the contents of files with a command. HkrsAI provides granular control over the OpenAI API's parameters. 

hkrsAI is modeled as a finite state machine, allowing you to perpetually engage in conversations with custom AIs for any circumstance. The program includes 100's of premade system prompts from the most popular repos on Github. You can set a custom prompt, or select from pre-made fonts from a convenient menu. You can reset the conversation at any time, and input a new font. The program is also scriptable, and command-line arguments can control any of the API parameters at runtime.

Version 2 is thanks to guidance (code reviews) that I received from a dear friend with a PHD in Computer Science and a decade of career experience working as a ML scientist at DeepMind. Thanks to his guidance the code is much more portable. You can easily extend HkrsAI by adding a new function to the Dispatcher class (with a matching signature), and adding its name to the command-list in the Parser class.

I built hkrsAI as a daily use productivity tool for myself, and I absolutely love it. I hope you will too!

---
   
# Index

1. [Getting-Started](#Getting-Started)
2. [At-Runtime](#At-Runtime)
3. [Command-Line-Arguments](#Command-Line-Arguments)
4. [System-Prompts](#System-Prompts)
5. [Logging](#Logging)
6. [Workflow-Integration](#Workflow-Integration)
7. [Context-Management-Commands](#Context-Management-Commands)

----

<!-- GETTING STARTED -->
## Getting Started:

hkrsAI uses one non-standard Python Library, the OpenAI lib: [https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)


**Installation**

Youtube installation and usage demo: [https://youtu.be/NF72un9Ie0c?si=Ys_U4qexGgQG88KS](https://youtu.be/NF72un9Ie0c?si=Ys_U4qexGgQG88KS)

1. Get an API Key at [https://platform.openai.com/signup](https://platform.openai.com/signup)](https://platform.openai.com/signup)
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
   ./hkrsai.py 
   ```
5. Input your API key when prompted (your key will be saved in the program's parent directory in config.json).
6. Define a custom system prompt, or select a pre-made prompt from 100's of premade options.
7. To view context management commands input '>help', after an AI assistant has been defined.

---

## At Runtime

At the beginning of each runtime, hkrsAI will check to see if the JSON config file and a logs directory are present in the program's parent directory. The config file tracks the current log number, and stores the user's API key for communicating with ChatGPT. If either the logs folder or config.json are missing the program will generate them. HkrsAI then checks for a stored API key. If none is found, it prompts you to input a new key. Everytime a new key is input, or the API key is retrieved from the config.json, hkrsAI will verify the key is valid with the OpenAI API. 

---

## Command Line Arguments

HkrsAI parses for a number of command-line arguments. The user is able to to set each of GPTs parameters, as well as logging-level, log format, and a path to a pre-made system prompt.

To view detailed information, use:


```python
./hkrsai.py -h
```


For detailed information on the each of GPTs parameters, please see the: [OpenAI API Documentation](https://platform.openai.com/docs/api-referen)

Example runtime arguments:


```bash
./hkrsai.py -sp ./prompts/fun/yoda -m gpt-4 --temperature 1.2 --max-tokens 200 --log-format txt
```


---

## System Prompts

System prompts are one of the most powerful tools you can use when interacting with ChatGPT. In a nutshell, system prompts allow you to define your AI's perosna, scope of knowledge, and format for output.

At the beginning of runtime, if no prompt was supplied via the command-line arguments, the user will be prompted to input a custom prompt, or hit 'enter' to select from the premade system prompts already built-in to the program. The pre-made system prompts were primarily ported from the Github repo, [Awesome-ChatGPT-Prompts](https://github.com/f/awesome-chatgpt-prompts), with an impressive 95,000 stars.

To edit the premade prompts (highly suggested as some contain generic first questions), simpy edit the associated file in it's respective category within the prompts directory. To add new prompts, place an extensionless text file in the folder best representing your prompt's category.The next time you set the system prompt in hkrsAI your new prompt will be waiting for you.

**Adding a new prompt:**

Save your system-prompt as text in a file without an extension. Place the file in the ./src/prompts/category that best suits your prompt. It will be available the next time you call >reset or start the program.

---

## Logging

By default, hkrsAI will log the messages generated back and forth to ChatGPT. The messages are stored in the Conversation class messages class instance variable. Controlling the log level can be done with the log level command line argument (see below). The default level is 2, which saves the messages as decribed. Alternatively, you can select log level 1, which will export the entire response object into the log file as a string variable whenever a function makes a call to the Logger class log() method. 

The options for log format are 'txt' or 'json'. If 'txt' is selected, the logs will be saved as human readable text. 

Both options can be set during runtime using the appropriate context management command.

**The logs directory** will be generated as ./src/logs. Any >save commands made that do not specify a path will write the save-file to the logs directory with a generic name. If the config.json file gets deleted, the logger will check to see if a file exists before saving a log, and in the case a file is found, will increment the log number until no file exists. 

---

## Workflow Integration

I built this program for myself, as a tool that I wanted. Each feature was created to serve me use cases, which are primarily developing and penetration testing. You are able to extract code (provided the AI assistant presents it in code blocks: ```{code}```) to a relative or absolute location. You can execute system-wide commands for directory traversal, some of which don't work by default in the Python shell, like 'cd' and 'cat'. You can insert the contents of a file with a command, or copy+paste without sending unwanted requests to the GPT API (while thinking=True).

---

## Context Management Commands

The program's context management commands are designed specifically to enable integrating ChatGPT into the workflow of programmers and pentesters. 

---

**>stop** 

**info:** Sets thinking=True, halting messages being sent to GPT. While thinking=True, \
new inputs are appended to the query with a '\n', allowing the user to create a stacked query \
from X inputs. While thinking=True, the user is able to copy+paste to the program's Python \
shell, as well as use the '>insert' command (see below).

```
>stop
```

---

**>flush** 

**info:** While thinking=True, clears the value stored in the query. Aka, the fat fingers insurance 
clause.

```
>flush
```

---

**>insert** 

**info:** When thinking=True, '>insert' fetches the contents of a file and appends it to the query. Primarily a feature for developers to easily import code from their projects into the program, or to enable more advanced scripting capabilities.

```
>insert
>insert /absolute/path/filename.extension
>insert ./relative/path/filename.extension
```

---

**>start** 

**info:** Set thinking=False. The next input will trigger sending the stored query to GPT, \
resuming the conversation.

```
>start
```

---

**>exec** 

**info:** You can execute system-wide commands from within the program's Python shell. Note that 'cd', and 'cat' are hacked in. Many Linux programs will fail to execute. Primarily included to enable easy directory traversal for workflow integration.

```
>exec
>exec {system command} {args}
>exec cd ./logs  # cd to relative or absolute file path
>exec cd home  # returns to the hkrsAI parent directory
>exec ls -l
>exec cat ./filepath/filename.extension     # fetches and prints the contents of a file
```

---

**>save** 

**info:** Allows the user to extract and save code or text to relative, absolute, or generic file path.

```
>save
>save  # saves the AIs last reply to a generic save file
>save /path/filename.extension  # saves the AIs last reply to relative or absolute path
>save code  # extracts code from the last reply and saves it to a generic save file
>save code ./path/filename.extension  # extracts and saves code to a relative or absolute path
>save reply {None | /path/filename.extension}
>save response {None | /path/filename.extension}
>save messages {None | /path/filename.extension}
```

---

**>set** 

**info:** Changes the value with the associated parameter.

```
>set gpt {parameter} {value}
>set logger {level | format} 
>set {gpt_parameter} {value}  # for more information see ./hkrsai.py -h
>set {level} {value}  # levels: (1, 2)
>set {format} {value}  # format: ['json', 'txt']
```

---

**>show** 

**info:** Prints stored values to the console.

```
>show
>show  # prints the value stored in conversation.query
>show {conversation | gpt | logger } {key}
>show {gpt parameter}  # prints the value for a specific gpt parameter
>show  # prints the values stored in gpt and logger
>show gpt  # prints the values stored in gpt
```

---

**>reset** 

**info:** Allows the user to reset the conversation or start a new log.

```
>reset
>reset  # resets the AI assistant 
>reset conversation  # also resets the AI assistant
>reset log  # starts a new log file and maintains conversation
```

---

**>exit** 

**info:** Quit the program.

```
>exit
```

---
<!-- ROADMAP -->
## Roadmap

- [x] V1 - all features work (code is very ugly)
- [x] V2 - all features work (code is hopefully a lot less ugly)
- [x] V2 - Beta tester bughunt *in progress
- [ ] Add Additional features and integration based on user feedback
- [ ] Another one (next project time)

---

## Contact

If you have features, suggestions, or bugs, feel free to reach out to this email address. Please note that my last project was ransomware that was 8x faster than Conti's. Resist the urge to send phishing emails to me. 

This email is for projects only!
Wolf - 0x00w0lf@proton.me

</p>
Project Link: [https://github.com/0x00wolf/hkrsai](https://github.com/0x00wolf/hkrsai)
</center>
