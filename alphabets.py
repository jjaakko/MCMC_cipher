import string


class UnindentifiedLanguage(Exception):
    pass


def get(language_code):
    if language_code == "fi":
        alphabets = list(string.ascii_uppercase + "ÅÄÖ")
    elif language_code == "en":
        alphabets = list(string.ascii_uppercase)
    else:
        raise UnindentifiedLanguage(
            f"Can't proceed with language code: {language_code}"
        )
    return alphabets
