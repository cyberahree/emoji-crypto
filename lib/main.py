from string import ascii_lowercase, ascii_uppercase, digits
from itertools import product, cycle
from random import choices
from tqdm import tqdm
from math import log2

CHARSET = ascii_lowercase + ascii_uppercase + digits + " :_{}!()"
VALID_EMOJIS = ["👽", "😎", "🥳", "🤓", "😈", "😤", "🤬", "👍", "👎", "👺"]

def _shannon_entropy(s):
    prob = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * log2(p) for p in prob)

class EmojiEncode:
    def __init__(self, Password: str = None, PassLength: int = 14):
        if isinstance(Password, str):
            self._password = Password
            self._passlen = len(Password)
        elif isinstance(PassLength, int):
            self._password = choices(VALID_EMOJIS, k=PassLength)
            self._passlen = PassLength
        else:
            raise Exception("Password must be a string or PassLength must be an integer")

    def encode(self, text: str) -> str:
        assert set(text) <= set(CHARSET), "Provided text contains invalid characters"
        
        encrypted = ""

        for char, key_char in zip(text, cycle(self._password)):
            encrypted += chr(ord(char) + ord(key_char))

        return encrypted
    
    def decrypt(self, text: str, password: str = None) -> str:
        if password is None:
            password = self._password

        decrypted = ""

        for char, key_char in zip(text, cycle(password)):
            decrypted += chr(ord(char) - ord(key_char))

        assert set(decrypted) <= set(CHARSET), "Decrypted text contains invalid characters"

        return decrypted

    def known_prefix_recovery(self, text: str, prefix: str, password_len: int) -> list[str]:
        password = ""

        for index in tqdm(range(len(prefix)), desc="Recovering password"):
            char = text[index]

            for emoji in VALID_EMOJIS:
                result = ""

                try:
                    # this code either errors, or it works perfectly fine
                    # that's why the assertion has no message omegalul
                    result = chr(ord(char) - ord(emoji))
                    assert result in CHARSET
                except Exception as e:
                    pass

                if result != prefix[index]:
                    continue
                    #raise Exception(f"Prefix '{prefix}' not found in text '{text}'")
                
                password += emoji

        if len(password) < password_len:
            return self.progressive_recovery(
                text, password_len, {i: emoji for i, emoji in enumerate(password)}
            )
        elif len(password) == password_len:
            return self.decrypt(text, password)
        else:
            raise Exception(f"Password '{password}' is longer than expected '{password_len}'")

    def progressive_recovery(self, text: str, password_len: int, identified_emojis: list[str] = None) -> list[str]:
        incorrect_emojis = {i: set() for i in range(password_len)}
        combinations = {i: set() for i in range(password_len)}

        if identified_emojis is not None:
            for i in range(len(identified_emojis)):
                correct_emoji = identified_emojis[i]
                combinations[i].add(emoji)

                for emoji in VALID_EMOJIS:
                    if emoji == correct_emoji:
                        continue
                    
                    incorrect_emojis[i].add(emoji)

        # loop for every character in the provided text
        # try to decrypt it with every emoji combination
        # if it works, store the value at the modulo of the password length
        # if it fails, and the emoji is in the dict, remove it
        for i in tqdm(range(len(text)), desc="Recovering password"):
            char = text[i]
            
            # i know the following code is extremely expensive,
            # however; it works LOL (besides, it doesn't take too long
            # to actually run) -ari
            for emoji in VALID_EMOJIS:
                comb_position = i % password_len
                result = None

                try:
                    # this code either errors, or it works perfectly fine
                    # that's why the assertion has no message omegalul
                    result = chr(ord(char) - ord(emoji))
                    assert result in CHARSET
                except Exception as e:
                    incorrect_emojis[comb_position].add(emoji)
                    combinations[comb_position].discard(emoji)
                else:
                    if (emoji not in combinations[comb_position]) and (emoji not in incorrect_emojis[comb_position]):
                        combinations[comb_position].add(emoji)
        
        # this isn't the best, since we might have mutliple emojis for the same position
        # but we can generate all combinations of the emojis in the dict, and try to
        # decrypt the text with each combination, we can return a list of all the
        # combinations that work
        results = []

        for emojis in product(*combinations.values()):
            try:
                result = self.decrypt(text, emojis)
                assert set(result) <= set(CHARSET)
            except Exception as e:
                continue
            else:
                results.append(result)

        return sorted(results, key=_shannon_entropy)
            
if __name__ == "__main__":
    encoder = EmojiEncode()

    print(f"[!] Testing encoding and decoding with automatically generated password '{''.join(encoder._password)}'")

    encrypted = encoder.encode("ARIII{ar1_w0z_h323_hj42_hj42_hj42_hj42!!!!!1!}")
    decrypted = encoder.decrypt(encrypted)

    print(f"[>] Encrypted: '{encrypted}'")
    print(f"[>] Decrypted: '{decrypted}'")

    print(f"[!] Attempting to recover original text with known prefix")
    recovered = encoder.known_prefix_recovery(
        encrypted,
        "ZeroDays{ar",
        encoder._passlen
    )

    print(f"[>] Recovered: '{recovered}'")

    print(f"[!] Attempting to recover original text progressively")
    progressive = encoder.progressive_recovery(
        encrypted,
        encoder._passlen
    )

    print(f"[>] Recovered, top three: '{progressive[:3]}'")
    print("[:D] Done")
