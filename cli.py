from pathlib import Path
import json
import argparse
import adjacent_letters
import MCMC
import cipher
import alphabets


def compute_stats(args):
    print(f"Computing adjacent letter counts from {args.src[0]} ...")
    letter_counts = adjacent_letters.get_count_from_file(
        filename=Path(args.src[0]), language_code=args.lang[0]
    )
    destination = f"{args.dest[0]}_{args.lang[0]}.json"
    letter_counts_as_json: str = json.dumps(letter_counts, indent=4)
    with open(Path(destination), "w") as f:
        f.write(letter_counts_as_json)
        print(f"Adjacent letter counts written in {destination}")


def mcmc(args):
    with open(args.src[0]) as f:
        encrypted_text = f.read()

    mcmc = MCMC.SubstitutionCipherMCMC(args.lang[0])

    initial_cipher = cipher.create_random_cipher(mcmc.alphabets)
    mcmc_cipher, acr = mcmc.MCMC(
        encrypted_text, initial_cipher, iters=int(args.iters[0]), logging=500
    )
    print("\n\n")
    print(cipher.apply(encrypted_text, mcmc_cipher, mcmc.alphabets))
    print(f"ACR: {acr}")


def encrypt(args):
    alphabets_ = alphabets.get(args.lang[0])
    cipher_str: str = cipher.create_random_cipher(alphabets_)
    with open(args.src[0]) as f:
        text_to_encrypt = f.read()
    encrypted_text = cipher.apply(text_to_encrypt, cipher_str, alphabets_)
    with open(args.dest[0], "w") as f:
        f.write(encrypted_text)
    print("Encryted text: ")
    print(encrypted_text)
    print(f"Cipher: {cipher_str}")


if __name__ == "__main__":
    # Define command and options for computing adjacent letter counts.
    parser = argparse.ArgumentParser(
        description="Decrypt substitution cipher with MCMC"
    )
    subparsers = parser.add_subparsers()
    parser_a = subparsers.add_parser(
        "count_from_file", help="Count adjacent letters from a specified file."
    )
    parser_a.add_argument("--src", nargs=1, required=True)
    parser_a.add_argument("--dest", nargs=1, required=True)
    parser_a.add_argument("--lang", choices=["fi", "en"], nargs=1, required=True)
    parser_a.set_defaults(func=compute_stats)

    parser_b = subparsers.add_parser(
        "decrypt", help="Use MCMC to decrypt substitution cipher."
    )
    parser_b.add_argument(
        "--src", nargs=1, required=True, help="Filename containing the text to decrypt."
    )
    parser_b.add_argument(
        "--iters", nargs=1, required=True, help="Iterations to be used with MCMC."
    )
    parser_b.add_argument("--lang", choices=["fi", "en"], nargs=1, required=True)
    parser_b.set_defaults(func=mcmc)

    parser_c = subparsers.add_parser(
        "encrypt", help="Use MCMC to encrypt with a random substitution cipher."
    )
    parser_c.add_argument(
        "--src", nargs=1, required=True, help="Filename containing the text to encrypt."
    )
    parser_c.add_argument(
        "--dest", nargs=1, required=True, help="Filename for saving encrypted text."
    )
    parser_c.add_argument("--lang", choices=["fi", "en"], nargs=1, required=True)
    parser_c.set_defaults(func=encrypt)

    args = parser.parse_args()
    args.func(args)
