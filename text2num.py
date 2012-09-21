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
    'ninety': 90
}

MAGNITUDE = {
    'thousand':     1000,
    'million':      1E6,
    'billion':      1E9,
    'trillion':     1E12,
    'quadrillion':  1E15,
    'quintillion':  1E18,
    'sextillion':   1E21,
    'septillion':   1E24,
    'octillion':    1E27,
    'nonillion':    1E30,
    'decillion':    1E33,
}

class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def text2num(spelled_num):
    """
    >>> assert 1 == text2num("one")
    >>> assert 12 == text2num("twelve")
    >>> assert 72 == text2num("seventy-two")
    >>> assert 300 == text2num("Three hundred")
    >>> assert 1200 == text2num("TWELVE HUNDRED")
    >>> assert 12304 == text2num("twelve thousand three hundred four")
    >>> assert 6000000 == text2num("six Million")
    >>> assert 6400005 == text2num("six million four hundred thousand five")
    >>> assert 123456789012 == text2num('one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve')
    >>> assert 4E33 == text2num("four decillion")
    """
    words = re.split(r"[\s-]+", spelled_num.lower())
    major = 0
    units = 0
    for w in words:
        x = SMALL.get(w, None)
        if x is not None:
            units += x
        elif w == "hundred":
            units *= 100
        else:
            x = MAGNITUDE.get(w, None)
            if x is not None:
                major += units * x
                units = 0
            else:
                raise NumberException("Unknown number: %s" % w)
    return major + units
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()