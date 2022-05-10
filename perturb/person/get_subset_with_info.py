"""
Input: dev_answer_entity.jsonl, which stores **the entities in the answers** for each instance if exists
Output: person/genderized_name.jsonl, which stores **genderilzed two-word person name in the answer** for each instance if exists
"""
import json
import os
import argparse

import gender_guesser.detector as gender

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--in_filename', default='dev_answer_entity.jsonl')
parser.add_argument('--out_filename', default='answer_entity_with_info.jsonl')

args = parser.parse_args()

in_path = f'{args.base_folder}/{args.dataset}/{args.in_filename}'
out_path = f'{args.base_folder}/{args.dataset}/person/{args.out_filename}'

os.makedirs(f'{args.base_folder}/{args.dataset}/person', exist_ok=True)
output_dict_lst = []
d = gender.Detector(case_sensitive=False)

with open(in_path, 'r', encoding="utf-8") as f_in:
    data_lst = [json.loads(line) for line in f_in]
for data in data_lst:
    if 'PERSON' in data['answer_entities']:
        person_lst = data['answer_entities']['PERSON']
        filtered_person_lst = []
        for person_name in person_lst:
            if len(person_name.split(' ')) <= 2:
                filtered_person_lst.append(person_name)
        if len(filtered_person_lst) > 0:
            idx = data['idx']
            names = []
            for name in filtered_person_lst:
                name_word_lst = name.split(' ')
                if len(name_word_lst) == 1:
                    first_name = name_word_lst[0]
                elif len(name_word_lst) == 2:
                    first_name, last_name = name_word_lst
                else:
                    raise ValueError()
                ret = d.get_gender(first_name)
                if ret in ['male', 'mostly_male']:
                    gender = 'M'
                elif ret in ['female', 'mostly_female']:
                    gender = 'F'
                else:
                    gender = 'N'
                if len(name_word_lst) == 1:
                    names.append([gender, first_name])
                elif len(name_word_lst) == 2:
                    names.append([gender, first_name, last_name])
                else:
                    raise ValueError()
            output_dict = {'idx': idx, 'names': names}
            output_dict_lst.append(output_dict)

with open(out_path, 'w', encoding='utf-8') as f_out:
    for data in output_dict_lst:
        f_out.write(json.dumps(data) + '\n')
