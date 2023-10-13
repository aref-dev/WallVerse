import random
import cowsay
from database import DataBase


def wider_cowsay_wrap_lines(lines, max_width=90):
    """Here, because the cowsay package has a default max_width of 49 for its wrap_line function, I'm using
     Monkey Patching to increase the max_width to 100 to prevent distortions. """
    new_lines = []
    for line in lines:
        for line_part in [
            line[i:i + max_width] for i in range(0, len(line), max_width)
        ]:
            new_lines.append(line_part)
    return new_lines


# Replacing cowsay function with a custom one.
cowsay.main.wrap_lines = wider_cowsay_wrap_lines


class QuoteGen:
    def __init__(self):
        self.db = DataBase()
        self.random_quote = None
        self.cowsay_string = None
        self.quote_pack = None

    def get_random_quote(self):
        if self.quote_pack == "custom":
            filepath = 'quote_packs/custom.txt'
            with open(filepath) as file:
                file_data = file.read().split('\n')
                random_quote = random.choice(file_data)
                self.random_quote = random_quote
                return self.random_quote
        else:
            self.random_quote = self.db.fetch_random_quote(self.quote_pack)
            return self.random_quote

    def set_quote_pack(self, quote_pack):
        self.quote_pack = quote_pack

    def pass_to_cowsay(self, input_text=None, cowsay_character="cow"):
        self.cowsay_string = cowsay.get_output_string(char_name=cowsay_character, text=input_text)
        return self.cowsay_string
