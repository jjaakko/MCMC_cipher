import math
import json
import random
from pathlib import Path
from typing import Tuple
import cipher
from custom_types import CountDict
import adjacent_letters
import alphabets


def load_json_from_file(filename: Path) -> CountDict:
    with open(filename) as f:
        content = f.read()
    stats = json.loads(content)
    return stats


class SubstitutionCipherMCMC:
    """Provide class for performing decryption using MCMC with Metropolis-Hastings algorithm."""

    def __init__(self, language_code):
        self.alphabets = alphabets.get(language_code)
        self.stats: CountDict = load_json_from_file(
            f"letter_counts_{language_code}.json"
        )

    def get_cipher_score(self, encrypted_text: str, cipher_text: str) -> float:
        """Apply the cipher to the encrypted text and compute the probability of the
        decrypted text, given alphabet and statistics per defined language.

        Returns:
            float: Score, that is, unnormalized log probability of the decrypted text given certain
            language.
        """
        decrypted_text = cipher.apply(encrypted_text, cipher_text, self.alphabets)
        counts_dict = adjacent_letters.get_count(decrypted_text, self.alphabets)
        score = 0.0
        for k, v in counts_dict.items():
            if k in self.stats:
                score += v * math.log(self.stats[k])
        return score

    def get_new_cipher_proposal(self, cipher_text: str) -> str:
        """Propose a new cipher by switching the positions of two random letters in the cipher.

        Args:
            cipher_text (str): Cipher as a string.

        Returns:
            str: New cipher.
        """
        cipher = list(cipher_text)
        pos1 = random.randint(0, len(cipher) - 1)
        pos2 = random.randint(0, len(cipher) - 1)
        if pos1 == pos2:
            return self.get_new_cipher_proposal(cipher_text)
        else:
            pos1_alpha = cipher[pos1]
            pos2_alpha = cipher[pos2]
            cipher[pos1] = pos2_alpha
            cipher[pos2] = pos1_alpha

        return "".join(cipher)

    def random_coin(self, p: float) -> bool:
        """Toss a coin with probability of heads being p"""
        unif = random.uniform(0, 1)
        if unif >= p:
            return False
        else:
            return True

    def MCMC(
        self, encrypted_text: str, init: str, iters: int, logging: int = 500
    ) -> Tuple[str, float]:
        """Try to decrypt encrypted text with metropolis-hastings algorithm.

        Args:
            encrypted_text (str): Text to decrypt.
            init (str): Initial cipher for the algorithm.
            iters (int): Number of iterations/samples.
            logging (int, optional): Display logging information every n iterations where
            logging specifies n.

        Returns:
            Tuple[str, float]: The most probable cipher, acceptance rate of the sampler.
        """
        current_cipher = init
        best_cipher = init
        max_score = 0.0
        accepted = 0
        for i in range(iters):
            cipher_proposal = self.get_new_cipher_proposal(current_cipher)
            score_current_cipher = self.get_cipher_score(encrypted_text, current_cipher)
            score_proposed_cipher = self.get_cipher_score(
                encrypted_text, cipher_proposal
            )
            try:
                acceptance_probability = min(
                    1, math.exp(score_proposed_cipher - score_current_cipher)
                )
            except OverflowError:
                acceptance_probability = 1

            if score_current_cipher > max_score:
                best_cipher = current_cipher
                max_score = score_current_cipher
            if self.random_coin(acceptance_probability):
                current_cipher = cipher_proposal
                accepted += 1
            if logging and i % logging == 0:
                msg = self.log(encrypted_text, i, best_cipher, accepted)
                print(msg)
        return best_cipher, accepted / iters

    def log(self, encrypted_text, i, best_cipher, accepted):
        log_info = f"Iteration: {i}\nDecrypted text with best cipher so far: {cipher.apply(encrypted_text, best_cipher, self.alphabets)[0:60]}\n"
        if i > 0:
            log_info += f"accept rate: {accepted/i:.2f}\n"
        return log_info
