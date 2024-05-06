import tkinter as tk
from tkinter import scrolledtext
import re
import random

class TextEncoderDecoderApp:
    def __init__(self, master):
        self.master = master
        master.title("Text Encoder Decoder")

        self.textbox = scrolledtext.ScrolledText(master, width=80, height=50)
        self.textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.encode_button = tk.Button(master, text="Encode", command=self.encodeText)
        self.encode_button.pack(side=tk.TOP, padx=10, pady=10)

        self.decode_button = tk.Button(master, text="Decode", command=self.decodeText)
        self.decode_button.pack(side=tk.TOP, padx=10, pady=10)

        self.pattern = r'\d+|\n+|\t+|in|==|-|===|>=|!=|<=|&&|\|\||[][()[\]"}}{. ,!><#@;*+&:|\'\[\]]|->|=|[a-zA-Z_]\w*'
        self.code = ""
        self.toEncode = []
        self.toDecode = []
        self.randomNumber = {}

    def encodeText(self):
        self.code = self.textbox.get("1.0", tk.END)

        # Find all matches
        matches = re.findall(self.pattern, self.code)

        for match in matches:
            # Check if the match already has a random number assigned
            if match not in self.randomNumber:
                randomNumber = random.randint(100, 999)
                while randomNumber in self.randomNumber.values():  # Ensure unique random numbers
                    randomNumber = random.randint(100, 999)
                self.randomNumber[match] = randomNumber

            self.toEncode.append(str(self.randomNumber[match]))

        # Clear the textbox
        self.textbox.delete("1.0", tk.END)

        # Insert the encoded numbers into the textbox
        self.textbox.insert(tk.END, ' '.join(self.toEncode))  # Separate encoded numbers by space

    def decodeText(self):
        # Get the encoded text from the textbox
        encoded_text = self.textbox.get("1.0", tk.END)

        # Split the encoded text into individual encoded elements
        encoded_elements = encoded_text.split()

        # Iterate over each encoded element
        decoded_text = ""
        for element in encoded_elements:
            # Iterate over the random number dictionary to find the corresponding original text
            for key, value in self.randomNumber.items():
                if str(value) == element:
                    decoded_text += key  # Add space after each decoded word/symbol
                    break

        # Clear the textbox
        self.textbox.delete("1.0", tk.END)

        # Insert the decoded text into the textbox
        self.textbox.insert(tk.END, decoded_text)



