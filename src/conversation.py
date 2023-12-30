import dataclasses
import openai
from typing import List
from src.systemprompt import SystemPrompt
from src.gpt import GPT


@dataclasses.dataclass
class Conversation:
    messages: list[dict] = dataclasses.field(default_factory=list)
    query: str = ''
    reply: str = ''
    response: dict = dataclasses.field(default_factory=dict)
    tokens: int = 0

    def start(self, system_prompt: str):
        self.messages = [{"role": "system", "content": system_prompt}]
        print()
        return Conversation(messages=self.messages)

    def speak(self, content: str):
        self.messages.append({"role": "user", "content": content})
        return Conversation(messages=self.messages, query=self.query, reply=self.reply, response=self.response)

    def think(self, thought):
        if self.query == '':
            self.query = thought
        else:
            self.query = f'{self.query}\n{thought}'
        return Conversation(messages=self.messages, query=self.query, reply=self.reply, response=self.response)

    def listen(self, gpt: GPT):
        """Function to perform GPT chat completions via the API"""
        self.response = gpt.client.chat.completions.create(
            model=gpt.model,
            messages=self.messages,
            temperature=gpt.temperature,
            top_p=gpt.top_p,
            n=gpt.n,
            max_tokens=gpt.max_tokens,
            frequency_penalty=gpt.frequency_penalty,
            presence_penalty=gpt.presence_penalty,
        )
        self.reply = self.response.choices[0].message.content
        self.tokens = self.response.usage.total_tokens
        print(f"\n{self.reply}\n")
        self.messages.append({"role": "assistant", "content": self.reply})

        return Conversation(messages=self.messages, query=self.query, reply=self.reply, response=self.response)

    def breath(self):
        return Conversation(messages=self.messages, query='', reply=self.reply, response=self.response)

    @staticmethod
    def greet():
        return Conversation(messages=[], query='', reply='', response=None)