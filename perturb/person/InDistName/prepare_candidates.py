import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../../../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--in_data_with_info', default='answer_entity_with_info.jsonl')
parser.add_argument('--out_candidates_folder_name', default='InDistName')
args = parser.parse_args()

in_data_with_info_path = f'{args.base_folder}/{args.dataset}/person/{args.in_data_with_info}'
output_folder_path = f'{args.base_folder}/{args.dataset}/person/{args.out_candidates_folder_name}'
os.makedirs(output_folder_path, exist_ok=True)

last_name_lst = []
male_first_name_lst = []
female_first_name_lst = []
neutral_first_name_lst = []
with open(in_data_with_info_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        for tup in data['names']:
            if len(tup) == 2:
                gender, first_name = tup
            elif len(tup) == 3:
                gender, first_name, last_name = tup
                last_name_lst.append(last_name.title())
            else:
                raise ValueError()
            if gender == 'M':
                male_first_name_lst.append(first_name.title())
            elif gender == 'F':
                female_first_name_lst.append(first_name.title())
            elif gender == 'N':
                neutral_first_name_lst.append(first_name.title())
            else:
                raise ValueError()

output_dict = {
    'first_name_male': male_first_name_lst,
    'first_name_female': female_first_name_lst,
    'first_name_neutral': neutral_first_name_lst,
    'last_name': last_name_lst
}
with open(f'{output_folder_path}/candidate_names.json', 'w', encoding='utf-8') as f:
    json.dump(output_dict, f, indent=0, sort_keys=True)
