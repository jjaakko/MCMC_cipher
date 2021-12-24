import numpy.random as npr
from typing import List, Tuple
from custom_types import CipherDict


def create_cipher_dict(
    cipher: str, alphabets: List[str]
) -> Tuple[CipherDict, CipherDict]:
    """Create a mapping through which text can be encrypted .

    Args:
        cipher ([type]): [description]

    Returns:
        tuple: [description]
    """
    cipher_dict = {}
    decipher_dict = {}
    for i in range(len(cipher)):
        cipher_dict[alphabets[i]] = cipher[i]
        decipher_dict[cipher[i]] = alphabets[i]
    return cipher_dict, decipher_dict


def apply(text_to_encrypt: str, cipher: str, alphabets: List[str]) -> str:
    """Encrypts text with the provided cipher.

    Args:
        text_to_encrypt (str): [description]
        cipher (str): [description]

    Returns:
        str: [description]
    """
    cipher_dict, _ = create_cipher_dict(cipher, alphabets)
    text = list(text_to_encrypt)
    newtext = ""
    for elem in text:
        if elem.upper() in cipher_dict:
            newtext += cipher_dict[elem.upper()]
        else:
            newtext += " "
    return newtext


def create_random_cipher(alphabets: List[str]):
    cipher = "".join(npr.choice(alphabets, size=len(alphabets), replace=False))
    return cipher
