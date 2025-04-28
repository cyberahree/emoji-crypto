# emoji-crypto

This Python script ([`lib/main.py`](lib/main.py)) implements a simple text encoding and decoding mechanism using emoji-based passwords. It also includes functionality to attempt password recovery under certain conditions.

```bash
[>] Encrypted: '🥔📌🥵🦼🙗📸🙯🚀🥄📜🚅👾🦍💬🥻💭🥞🦦🙭📥🙸🙂🥅📜🙶💸🥇👿🥲📢🦖🦧🙀📜🙶🙸🥇💯😯👯🤴👮🤴💫🥍🧰'
[>] Decrypted: 'ARIII{ar1_w0z_h323_hj42_hj42_hj42_hj42!!!!!1!}'
```

## Features
*   **Encoding**: Encodes text by adding the ordinal value of each character with the ordinal value of a corresponding character from an emoji password (cycling through the password).
*   **Decoding**: Reverses the encoding process to retrieve the original text.
*   **Password Generation**: Can generate a random emoji password of a specified length using a predefined set of valid emojis (`VALID_EMOJIS`).
*   **Known Prefix Recovery**: Attempts to recover the emoji password if a prefix of the original plaintext is known ([`EmojiEncode.known_prefix_recovery`](lib/main.py#L48)).
*   **Progressive Recovery**: Attempts to recover the password by systematically trying valid emojis for each password position and validating the resulting decoded characters against an allowed character set (`CHARSET`). It uses Shannon entropy ([`_shannon_entropy`](lib/main.py#L10)) to rank potential decryptions ([`EmojiEncode.progressive_recovery`](lib/main.py#L80)).

```bash
[!] Attempting to recover original text with known prefix
[>] Recovered: ['ARIII{ar1_w0z_h323_hj42_hj42_hj42_hj42!!!!!1!}', 'ARIII{ar1bw0z_h323_hj42bhj42_hj42_hj45!!!!!1!}']
[!] Attempting to recover original text progressively
[>] Recovered, top three: ['ARIII{ar1_w0z_h323_hj42_hj42_hj42_hj42!!!!!1!}', 'ARIII{Kr1_w0z_h323_hT42_hj42_hj42_Rj42!!!!!1!}', 'ARIII{ax1_w0z_h323_hj:2_hj42_hj42_hp42!!!!!1!}']
```

## Usage

1.  Instantiate the `EmojiEncode` class, either providing a specific emoji password or a desired password length for random generation.
2.  Use the `encode` method to encrypt text.
3.  Use the `decode` method to decrypt text, providing the correct password if it wasn't stored in the instance.
4.  Use the recovery methods (`known_prefix_recovery` or `progressive_recovery`) to attempt finding the password for a given ciphertext.

The script defines `CHARSET` (allowed characters in plaintext/decrypted text) and `VALID_EMOJIS` (allowed emojis for passwords).

Refer to the `if __name__ == "__main__":` block within [`lib/main.py`](lib/main.py#L138) for example usage of encoding, decoding, and recovery methods.
