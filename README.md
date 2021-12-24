This project demonstrates how Markov chain Monte Carlo methods can be used to decrypt messages encrypted with a substitution cipher. Idea and some of the code adapted from this ![blogpost](https://towardsdatascience.com/applications-of-mcmc-for-cryptography-and-optimization-1f99222b7132)

## Usage

- Clone/download this repository
- Create and activate a virtual environment and run `pip install -r requirements.txt`
- Place a file containing a plain text in the project root
- Encrypt the contents of the file with randon substitution cipher by running `python cli.py encrypt --src [file with plain text] --dest [target file] --lang en`
- Use Metropolis-Hastings algorithm for decrypting the message by running `python cli.py decrypt --src [file with encrypted text] --iters 10000 --lang en`

- Note: `letter_counts_en.json` and `letter_counts_fi.json` contain adjacent letter counts for a large body of text for english and finnish respectively. Run `python cli.py count_from_file --src [text file] --dest letter_counts --lang en` if you want to count adjacent letters from a new english source.
