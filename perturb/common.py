person_prefix_lst = [
    "Adm", "Atty", "Brother", "Capt", "Chief", "Cmdr", "Col", "Dean", "Dr", "Elder", "Father", "Gen", "Gov", "Hon",
    "Lt Col", "Maj", "MSgt", "Mr", "Mrs", "Ms", "Prince", "Prof", "Professor", "Rabbi", "Rev", "Sister", "Miss",
]
person_prefix_lst = [f'{prefix.lower()} ' for prefix in person_prefix_lst] + \
                    [f'{prefix.lower()}. ' for prefix in person_prefix_lst]
person_suffix_lst = [
    'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
    'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX',
    'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX',
    'CPA', 'DDS', 'Esq', 'JD', 'Jr', 'LLD', 'MD', 'PhD', 'Ret', 'RN', 'Sr', 'DO'
]
person_suffix_lst = [f' {suffix.lower()}' for suffix in person_suffix_lst] + \
                    [f' {suffix.lower()}.' for suffix in person_suffix_lst]


def normalize_entity_name(entity_name, entity_type):
    s = entity_name.lower().strip()
    for outer_prefix in ["the "]:
        if s.startswith(outer_prefix):
            s = s[len(outer_prefix):].strip()
    if entity_type == 'PERSON':
        for outer_suffix in ["'", "'s", ":"]:
            if s.endswith(outer_suffix):
                s = s[:-len(outer_suffix)].strip()
        for prefix in person_prefix_lst:
            if s.startswith(prefix):
                s = s[len(prefix):].strip()
        for suffix in person_suffix_lst:
            if s.endswith(suffix):
                s = s[:-len(suffix)].strip()
    elif entity_type == 'ORG':
        pass
    elif entity_type == 'DATE':
        pass
    elif entity_type == 'GPE':
        pass
    return s.strip()
