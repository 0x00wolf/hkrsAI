

<!-- ABOUT THE PROJECT -->
# **hkrsAI.v2**

Version 2 is out!

## The keep it simple approach to integrating the world's most powerful AI into your Linux terminal.

In the principle of KISS (not the band), I wanted a tool that integrated seamlessly into my development workflow, but streamlined enough to fit nicely into a single Python file (with a second to contain long string variables). I wanted to be able to copy+paste, insert files with a single command, execute system wide commands for directory traversal, have automatic logging in case I wanted to come back to something, but didn't remember to save it, and the ability to extract code easily.

hkrsAI is modeled as a finite state machine, allowing you to perpetually engage in conversations with custom AIs for any circumstance. The program includes 100's of premade system prompts from the most popular repos on Github (thanks to https://github.com/f/awesome-chatgpt-prompts), which can be selected via a convenient menu system at anytime within the program.

I built hkrsAI as a daily use productivity tool for myself, and I absolutely love it. I hope you will too!

---
<!-- GETTING STARTED -->
### Getting started:

hkrsAI uses one non-standard Python Library, the OpenAI lib: [https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)

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
   ./hkrsai.py 
   ```
5. Input your API when prompted.
6. Select a premad system prompt or input your own.
7. Once a system prompt has been entered, input '>' to view the context management commands manual (or see below).
---
### First Runtime

The first time you run hkrsAI it will generate JSON config file in the parent directory. The config file tracks log numbers, and stores the user's API key for communicating with ChatGPT. By default, hkrsAI will check for a key and prompt you to insert one if none is present. The program also verifies the validity of keys at boot up, or anyitme you initate a new chat session.

Logfiles will be saved in the logs folder in the parent directory. This will also be generated on the first runtime.

---
### Command Line Arguments

The command line arguments include each GPT's API parameters, as well as logging-level, log format, and system prompt.

To view detailed information about hkrsAI's runtime parameters in the terminal, you can input:

```python
./hkrsai.py -h
```

Although you can find detailed information in the help strings on each of the parameters and their functions, explaining their individual use case is beyond the scope of this README.md. Please see the: [OpenAI API Documentation](https://platform.openai.com/docs/api-referen)

Example runtime arguments:

```bash
./hkrsai.py -sp ./prompts/fun/yoda --temperature 1.2 --max-tokens 200 --log-format txt
```
---

### System Prompts

System prompts are one of the most powerful tools you can use when interacting with ChatGPT. In a nutshell, system prompts allow you to define the scope of knowledge of your AI assistant, it's personality, and it's format for responses.

To edit the premade prompts (highly suggested as some contain generic first questions), simpy edit the associated file in it's respective category within the prompts directory. To add new prompts all you have to do is place a text file with your desired prompt in the category of your choosing. The next time you set the system prompt in hkrsAI your new prompt will be waiting for you.

### Context Management Commands

**>stop**

```
>stop
```

info:
  - Sets the pocketAI class variable freeze=True, allowing the user to stack a query with multiple inputs.
  - When freeze=True, you can copy+paste code to the hkrsAI's Python shell. You can also
  - Allows the user to build a query from a series of inputs, with each input parsed for state commands.
  - Users can insert the contents of a file into their query, while freeze=True with the '>insert' command (see below).
---

**>start**  

```
>start
```

info:
   - Sets freeze=False. 
   - Hit enter when the prompt returns to submit the query to the GPT API.
   - Note that some commands only work when freeze=True (copy+pasting and >insert).
---


**>exec**

```
>exec {system_command} {args[1:]}
>exec ls -l
>exec cd ../
>exec pwd
>exec cat /pathto/file.extension
```
info:
   - Allows the user to execute system commands within pocketAI's shell.
   - Any additional arguments in the input will be executed as a system commands.
   - Note that the program runs in a Python shell, which technically doesn't have access to the 'cd' command,
      but 'cd' and 'cat' have been included with a little hack.
   - The primary function of being able to execute system commands is directory traversal and organizing files.
---

**>insert**  

```
>insert  /path/to/file.extension
>insert ./filename.extension
```
info:
   - Fetches the contents of a file and appends it to the query.
   - Requires freeze=True.
---

**>reset**

```
>reset
```       
info:
- Resets the system prompt, generates a new log, and initiates a new chat session.
- Note: This command will also clear the current query, and messages. Before a new command is sent to the GPT
API the user is still able to save the previous response, which will be replaced with the response from the API.

---

**>show**

```
>show
>show temperature
>show gpt
>show vars
>show query
>show response
>show tokens
```

info:
   - By default, inputting '>show' or '>print' will print the contents of the current query saved in memory. 
   - By adding an additional arguments, pocketAI will display the values pertaining to that value.
   - 'vars' prints all of the set values for ChatGPT's parameters.
   - 'var' displays a specific parameter, which the user must specify.
---

**>flush**

```
>flush
```                    
info:
   - Resets the query to ''.
---

**>save**

```
>save code
>save code /path/to/savefile.extension
>save response
>save response ./path/filename.extensin
>save reply
```
info:
   - Allows the user to save the current response, messages, last reply, or extract and save code from the last reply.
   - The reply and messages can be saved in either human readable text, or formatted JSON output. 
   - To select a format, append the appropriate suffix to the file path argument.
----

**>exit**
 
```
>exit
```                     
info:
   - Quit the program.
----

<!-- ROADMAP -->
## Roadmap

- [x] Beta release
- [x] Beta tester bug hunt *in progress
- [ ] Add Additional features and integration based on user feedback
- [ ] Another one (next project time)

## Contact

If you have features, suggestions, or bugs, feel free to reach out to this email address. Please note that my last project was ransomware that was 8x faster than Conti's. Resist the urge to send phishing emails to me. 

This email is for projects only!
Wolf - 0x00w0lf@proton.me
Project Link: [https://github.com/0x00wolf/hkrsai](https://github.com/0x00wolf/hkrsai)
