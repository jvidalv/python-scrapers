import unicodedata


def delete_accents(string):
    s = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))
    return s
