import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../../../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--out_candidates_folder_name', default='IndianName')

args = parser.parse_args()

input_dictionary_genderized_first_name_json = f'genderized_indian_first_names.json'
input_last_name_csv = 'raw_data/surnames/surnames.csv'

output_folder_path = f'{args.base_folder}/{args.dataset}/person/{args.out_candidates_folder_name}'
os.makedirs(output_folder_path, exist_ok=True)

last_name_lst = []
with open(input_last_name_csv, 'r', encoding='utf-8') as f:
    for line in f:
        last_name = line.strip()
        if '"' not in last_name:
            last_name_lst.append(last_name.title())
with open(input_dictionary_genderized_first_name_json, 'r', encoding='utf-8') as f:
    genderized_dic = json.load(f)
male_first_name_lst = list(map(lambda x: x.title(), genderized_dic['male']))
female_first_name_lst = list(map(lambda x: x.title(), genderized_dic['female']))
neutral_first_name_lst = list(map(lambda x: x.title(), genderized_dic['neutral']))

output_dict = {
    'first_name_male': male_first_name_lst,
    'first_name_female': female_first_name_lst,
    'first_name_neutral': neutral_first_name_lst,
    'last_name': last_name_lst
}
with open(f'{output_folder_path}/candidate_names.json', 'w', encoding='utf-8') as f:
    json.dump(output_dict, f, indent=0, sort_keys=True)
