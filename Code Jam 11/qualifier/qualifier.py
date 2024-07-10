from enum import auto, StrEnum
import warnings
import re

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode

    def __str__(self) -> str:
        return self._create_variant()

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """
        if self.mode == VariantMode.UWU:
            if all(letter not in self.quote for letter in "LlRrUu"):
                raise ValueError("Quote was not modified")

            quote = (
                self.quote.replace("L", "W")
                .replace("l", "w")
                .replace("R", "W")
                .replace("r", "w")
            )

            u_quote = []
            for w in quote.split(" "):
                if w.startswith("U"):
                    w = "U-" + w
                elif w.startswith("u"):
                    w = "u-" + w
                u_quote.append(w)
            u_quote = " ".join(u_quote)

            if len(u_quote) > MAX_QUOTE_LENGTH:
                warnings.warn("Quote too long, only partially transformed")
                return quote

            return u_quote
        elif self.mode == VariantMode.PIGLATIN:
            VOWELS = "aeiou"
            words = []
            for word in self.quote.lower().split(" "):
                if word[0] in VOWELS:
                    words.append(word + "way")
                else:
                    v_pos = 0
                    for letter in word:
                        if letter in VOWELS:
                            break
                        v_pos += 1
                    words.append(word[v_pos:] + word[:v_pos] + "ay")

            quote = " ".join(words)
            quote = quote[0].upper() + quote[1:].lower()

            if len(quote) > MAX_QUOTE_LENGTH:
                raise ValueError("Quote was not modified")

            return quote
        elif self.mode == VariantMode.NORMAL:
            return self.quote


PATTERN = re.compile('["“](.*?)["”]')


def parse_quote(quote: str):
    r = PATTERN.search(quote)
    if r:
        if len(r.groups()[0]) > MAX_QUOTE_LENGTH:
            raise ValueError("Quote is too long")
        return r.groups()[0]


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """
    if command.startswith("quote list"):
        print("- " + "\n- ".join(Database.get_quotes()))
        return
    elif command.startswith("quote piglatin"):
        quote = parse_quote(command.split(" ", 2)[-1])
        mode = VariantMode.PIGLATIN
    elif command.startswith("quote uwu"):
        quote = parse_quote(command.split(" ", 2)[-1])
        mode = VariantMode.UWU
    elif command.startswith("quote"):
        quote = parse_quote(command.split(" ", 1)[-1])
        mode = VariantMode.NORMAL
    else:
        raise ValueError("Invalid command")

    if not quote:
        raise ValueError("Invalid command")

    try:
        Database.add_quote(Quote(quote, mode))
    except DuplicateError:
        print("Quote has already been added previously")


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
