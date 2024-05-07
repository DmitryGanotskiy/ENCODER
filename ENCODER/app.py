import tkinter as tk
from tkinter import scrolledtext
import re
import random
import json
from datetime import datetime

class TextEncoderDecoderApp:
    def __init__(self, master):
        self.master = master
        master.title("Text Encoder Decoder")

        self.textbox = scrolledtext.ScrolledText(master, width=80, height=50)
        self.textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.keyText = scrolledtext.ScrolledText(master, width=30, height=1)
        self.keyText.pack(side=tk.TOP, fill=tk.X, expand=False)

        tk.Label(master, text = "yyyy/mm/dd hh:mm").pack(side=tk.TOP, padx=10, pady=5)
        self.timeEntry = tk.Entry(master)
        self.timeEntry.pack(side=tk.TOP, padx=10, pady=5)

        self.encode_button = tk.Button(master, text="Encode", command=self.encodeText)
        self.encode_button.pack(side=tk.TOP, padx=10, pady=10)

        self.decode_button = tk.Button(master, text="Decode", command=self.decodeText)
        self.decode_button.pack(side=tk.TOP, padx=10, pady=10)

        self.pattern = r'\d+|\n+|\t+|in|==|-|===|>=|!=|<=|&&|\|\||[][()[\]"}}{. ,!><#@;*+&:|\'\[\]]|->|=|[a-zA-Z_]\w*'
        self.code = ""
        self.toEncode = []
        self.toDecode = []
        self.randomNumber = {}
        self.time = ""

        self.check()

    def check(self):
        currentTime = datetime.now()
        with open('dict.txt', 'r') as file:
            lines = file.readlines()
        with open('dict.txt', 'w') as file:
            for line in lines:
                dictData = json.loads(line)
                expired = False
                for key, value in dictData.items():
                    for dateString in value.keys():
                        date = datetime.strptime(dateString, '%Y/%m/%d %H:%M')
                        if date < currentTime:
                            expired = True
                            break
                    if not expired:
                        file.write(line)

    def encodeText(self):
        string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$&_-()=%*:/!?+."
        self.code = self.textbox.get("1.0", tk.END)

        if self.keyText.get("1.0", tk.END).strip():
            self.key = self.keyText.get("1.0", tk.END).strip()
            with open('dict.txt', 'r') as file:
                data = file.readlines()
                for line in data:
                    dict_data = json.loads(line)
                    if self.key in dict_data:
                        self.keyText.delete("1.0", tk.END)
                        self.key = "".join(random.sample(string, 40))
                        self.keyText.insert(tk.END, self.key)
        else:
            self.key = "".join(random.sample(string, 40))
            self.keyText.insert(tk.END, self.key)

        self.time = self.timeEntry.get()
        if not self.time:
            self.time = "9999/12/1 12:00"
            self.timeEntry.insert(tk.END, self.time)

        if self.key not in self.randomNumber:
            self.randomNumber[self.key] = {}
        self.randomNumber[self.key][self.time] = {}

        matches = re.findall(self.pattern, self.code)

        for match in matches:
            if match not in self.randomNumber[self.key][self.time]:
                randomNumber = random.randint(1, 999)
                while randomNumber in self.randomNumber[self.key][self.time].values():
                    randomNumber = random.randint(1, 999)
                self.randomNumber[self.key][self.time][match] = randomNumber

            self.toEncode.append(str(self.randomNumber[self.key][self.time][match]))

        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, ' '.join(self.toEncode))

        with open('dict.txt', 'a+') as file:
            json.dump({self.key: self.randomNumber[self.key]}, file)
            file.write('\n')

    def decodeText(self):
        key = self.keyText.get("1.0", tk.END).strip()
        encodedText = self.textbox.get("1.0", tk.END)
        encodedElements = encodedText.split()

        temp_dicts = []

        with open('dict.txt', 'r') as file:
            for line in file:
                decodedDict = json.loads(line)
                if key in decodedDict:
                    decodedText = ""
                    for element in encodedElements:
                        for time_key, values in decodedDict[key].items():
                            for k, v in values.items():
                                if str(v) == element:
                                    decodedText += k
                                    break

                    self.textbox.delete("1.0", tk.END)
                    self.textbox.insert(tk.END, decodedText)
                else:
                    temp_dicts.append(line)

        with open('dict.txt', 'w') as file:
            for line in temp_dicts:
                file.write(line)

