import re

SMALL = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,

    # ordinals
    'first': 1,
    'second': 2,
    'third': 3,
    'fourth': 4,
    'fifth': 5,
    'sixth': 6,
    'seventh': 7,
    'eighth': 8,
    'ninth': 9,
    'tenth': 10,
    'eleventh': 11,
    'twelfth': 12,
    'thirteenth': 13,
    'fourteenth': 14,
    'fifteenth': 15,
    'sixteenth': 16,
    'seventeenth': 17,
    'eighteenth': 18,
    'nineteenth': 19,
    'twentieth': 20,
    'thirtieth': 30,
    'fortieth': 40,
    'fiftieth': 50,
    'sixtieth': 60,
    'seventieth': 70,
    'eightieth': 80,
    'ninetieth': 90,
}

MAGNITUDE = {
    'thousand': 1000,
    'million': 10 ** 6,  # 10E6 gives a float
    'billion': 10 ** 9,
    'trillion': 10 ** 12,
    'quadrillion': 10 ** 15,
    'quintillion': 10 ** 18,
    'sextillion': 10 ** 21,
    'septillion': 10 ** 24,
    'octillion': 10 ** 27,
    'nonillion': 10 ** 30,
    'decillion': 10 ** 33,
}

_SINGLE_NUMBER_PTN = r'|'.join(re.escape(numword)
    for numword in list(SMALL.keys()) + list(MAGNITUDE.keys()) + ['hundred'])
SPELLED_NUMBER_RE = re.compile(r'\b(?:%s)(?:(?:,?\s+|-|\s+and\s+)(?:%s))*\b' % (
    _SINGLE_NUMBER_PTN, _SINGLE_NUMBER_PTN), re.IGNORECASE)


class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def spelled_num_to_digits(spelled_num):
    """
    >>> spelled_num_to_digits("one")
    1
    >>> spelled_num_to_digits("twelve")
    12
    >>> spelled_num_to_digits("seventy-two")
    72
    >>> spelled_num_to_digits("Three hundred")
    300
    >>> spelled_num_to_digits("TWELVE HUNDRED")
    1200
    >>> spelled_num_to_digits("twelve thousand three hundred four")
    12304
    >>> spelled_num_to_digits("twelve thousand, five hundred and six")
    12506
    >>> spelled_num_to_digits("six   Million")
    6000000
    >>> spelled_num_to_digits("250 million")
    250000000
    >>> spelled_num_to_digits("six million four hundred thousand five")
    6400005
    >>> spelled_num_to_digits(
    ...   'one hundred twenty three billion, four hundred fifty six million, '
    ...   'seven hundred eighty nine thousand twelve')
    123456789012
    >>> spelled_num_to_digits("four decillion")
    4000000000000000000000000000000000L
    >>> spelled_num_to_digits("4th")
    4
    """
    words = re.split(r",?\s+|-", spelled_num.lower())
    major = 0
    units = 0
    for w in words:
        x = SMALL.get(w, None)
        if x is not None:
            units += x
        elif w == "hundred":
            units *= 100
        elif w == "and":
            continue
        else:
            x = MAGNITUDE.get(w, None)
            if x is not None:
                major += units * x
                units = 0
                continue

            try:
                units += int(w)
                continue
            except ValueError:
                pass

            try:
                units += float(w)
                continue
            except ValueError:
                pass

            if w.endswith(("th", "st", "nd", "rd")):
                try:
                    # strip off ordinal th, st, nd, rd
                    units += int(w[:-2])
                    continue
                except ValueError:
                    pass

            raise NumberException("Unknown number: %s" % w)
    return major + units


def replace_spelled_numbers(sentence):
    """
    >>> replace_spelled_numbers('There are TEN sponges')
    'There are 10 sponges'
    >>> replace_spelled_numbers('I got ninety nine problems')
    'I got 99 problems'
    >>> replace_spelled_numbers('He got two million, one hundred and '
    ...   'eighty-two thousand, three hundred and twenty five problems')
    'He got 2182325 problems'
    >>> replace_spelled_numbers('I have five coconuts and two hundred '
    ...   'thirty three carrots')
    'I have 5 coconuts and 233 carrots'
    """
    def try_spelled_num_to_digits(text):
        try:
            return spelled_num_to_digits(text)
        except NumberException:
            return text
    return SPELLED_NUMBER_RE.sub(
        lambda m: str(try_spelled_num_to_digits(m.group())), sentence)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
