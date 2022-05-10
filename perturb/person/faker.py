import random
import string
import re


def _get_word_pattern(word):
    # possible patterns: ['aa', 'Aa', 'AA']
    first_char_pattern = None
    second_char_pattern = None
    for char in word:
        if char in string.ascii_letters:
            if char in string.ascii_lowercase:
                flag = 'a'
            else:
                flag = 'A'
            if first_char_pattern is None:
                first_char_pattern = flag
            elif first_char_pattern is not None and second_char_pattern is None:
                second_char_pattern = flag
                break
    if first_char_pattern is None:
        first_char_pattern = 'a'
    if second_char_pattern is None:
        second_char_pattern = 'a'
    if first_char_pattern == 'a':
        second_char_pattern = 'a'  # avoid 'aA'
    return f'{first_char_pattern}{second_char_pattern}'


def _convert_to_AA(word):
    return word.upper()


def _convert_to_Aa(word):
    return word.capitalize()


def _convert_to_aa(word):
    return word.lower()


def replace_in_doc(doc, src_word_lower, tgt_word):
    all_src = re.findall(re.escape(src_word_lower), doc, flags=re.IGNORECASE)  # enumerate all possible casing of src
    for src_surface_form in set(all_src):
        tgt_surface_form = tgt_word_formatter(tgt_word, src_surface_form)
        doc = doc.replace(src_surface_form, tgt_surface_form)
    return doc


def tgt_word_formatter(tgt_word, src_surface_form):
    # recase the tgt word based on the surface form of the src word
    word_pattern = _get_word_pattern(src_surface_form)
    tgt_word_lower = tgt_word.lower()
    if word_pattern == 'aa':
        return _convert_to_aa(tgt_word_lower)
    elif word_pattern == 'Aa':
        return _convert_to_Aa(tgt_word_lower)
    elif word_pattern == 'AA':
        return _convert_to_AA(tgt_word_lower)
    else:
        raise NotImplementedError()


def generate_randstr(src_word_lower):
    tgt_word_lower = src_word_lower[0]
    for char in src_word_lower[1:]:
        if char in string.ascii_letters:
            tgt_word_lower += random.choice(string.ascii_lowercase)
        else:
            tgt_word_lower += char
    if src_word_lower[-1] == 's':
        tgt_word_lower = tgt_word_lower[:-1] + 's'
    return tgt_word_lower
