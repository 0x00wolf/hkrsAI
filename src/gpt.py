import openai


BAD_MODEL= "[*] invalid option: if you are confident the model you are attempting to use is valid \
            please add it to the list in variables.py in the program's parent directory.\n"
BAD_TEMP = '[*] invalid temperature: {}\n[*] type=float, valid_range=(0, 2.0), default=0.7\n'
BAD_PP = '[*] invalid presence_penalty: {}\n[*] type=float, valid_range=(-2.0, 2.0), default=0]\n'
BAD_FP = '[*] invalid frequency_penalty: {}\n[*] type=float, valid_range=(-2.0, 2.0), default=0\n'
BAD_TP = '[*] invalid top_p: {}\n[*] type=float, valid_range=(0, 1.0), default=1.0\n'
BAD_N = '[*] invalid n: {}\n[*] type=int, valid_range=(1, 20), default=1.0\n'
BAD_MT = '[*] invalid max_tokens" {}\n[*] type=int, valid_range(1,4096), default=1.0\n'
MODELS = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo']


class GPT:
    def __init__(self, client, model, temperature, top_p, n, frequency_penalty, presence_penalty, max_tokens):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.max_tokens = max_tokens

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new_value: str):
        new_value = str(new_value)
        if new_value == 'gpt-3.5-turbo' or new_value == 'gpt-4':
            self._model = new_value
        else:
            raise ValueError(f'\n{BAD_MODEL.format(new_value)}')

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, new_value: float):
        new_value = float(new_value)
        if not (0.0 <= new_value <= 2.0):
            raise ValueError(f'\n{BAD_TEMP.format(new_value)}')
        else:
            self._temperature = new_value

    @property
    def top_p(self):
        return self._top_p

    @top_p.setter
    def top_p(self, new_value: float):
        new_value = float(new_value)
        if not (0 <= new_value <= 1.0):
            raise ValueError(f'\n{BAD_TP.format(new_value)}')
        else:
            self._top_p = new_value

    @property
    def frequency_penalty(self):
        return self._frequency_penalty

    @frequency_penalty.setter
    def frequency_penalty(self, new_value: float):
        new_value = float(new_value)
        if not (-2.0 <= new_value <= 2.0):
            raise ValueError(f'\n{BAD_FP.format(new_value)}')
        else:
            self._frequency_penalty = new_value

    @property
    def presence_penalty(self):
        return self._presence_penalty

    @presence_penalty.setter
    def presence_penalty(self, new_value: float):
        new_value = float(new_value)
        if not (-2.0 <= new_value <= 2.0):
            raise ValueError(f'\n{BAD_PP.format(new_value)}')
        else:
            self._presence_penalty = new_value

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, new_value):
        new_value = int(new_value)
        if not (1 <= new_value <= 20):
            raise ValueError(f'\n{BAD_N.format(new_value)}')
        else:
            self._n = new_value

    @property
    def max_tokens(self):
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, new_value: int):
        new_value = int(new_value)
        if not (1 <= new_value <= 4096):
            raise ValueError(f'\n{BAD_MT.format(new_value)}')
        else:
            self._max_tokens = new_value


