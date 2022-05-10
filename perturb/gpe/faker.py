import random
import string
import re


def mimic_casing(tgt_word, src_surface_form):
    assert len(tgt_word) == len(src_surface_form)
    tgt_surface_form = ''
    for tgt_char, src_char in zip(tgt_word, src_surface_form):
        if src_char.isupper():
            tgt_surface_form += tgt_char.upper()
        elif src_char.islower():
            tgt_surface_form += tgt_char.lower()
        else:
            tgt_surface_form += tgt_char
    return tgt_surface_form


def replace_in_doc_randstr(doc, src_word, tgt_word):
    all_src = re.findall(re.escape(src_word), doc, flags=re.IGNORECASE)  # enumerate all possible casing of src
    for src_surface_form in set(all_src):
        tgt_surface_form = mimic_casing(tgt_word, src_surface_form)
        doc = doc.replace(src_surface_form, tgt_surface_form)
    return doc


def generate_randstr(src_word):
    src_word_lower = src_word.lower()
    tgt_word_lower = src_word_lower[0]
    for char in src_word_lower[1:]:
        if char in string.ascii_letters:
            tgt_word_lower += random.choice(string.ascii_lowercase)
        else:
            tgt_word_lower += char
    if src_word_lower[-1] == 's':
        tgt_word_lower = tgt_word_lower[:-1] + 's'
    return tgt_word_lower


def replace_in_doc_phrase(doc, src_phrase, tgt_phrase):
    all_src = re.findall(re.escape(src_phrase), doc, flags=re.IGNORECASE)  # enumerate all possible casing of src
    for src_surface_form in set(all_src):
        tgt_surface_form = tgt_phrase_formatter(tgt_phrase, src_surface_form)
        doc = doc.replace(src_surface_form, tgt_surface_form)
    return doc


def tgt_phrase_formatter(tgt_phrase, src_surface_form):
    # recase the tgt phrase based on the surface form of the src phrase
    if all([char in f'{string.ascii_uppercase} {string.punctuation}' for char in src_surface_form]):
        return tgt_phrase.upper()
    elif all([char in f'{string.ascii_lowercase} {string.punctuation}' for char in src_surface_form]):
        return tgt_phrase.lower()
    else:
        return tgt_phrase
