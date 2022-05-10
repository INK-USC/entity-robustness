import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../../../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--in_data_with_info', default='answer_entity_with_info.jsonl')
parser.add_argument('--out_candidates_folder_name', default='InDistName')
args = parser.parse_args()

in_data_with_info_path = f'{args.base_folder}/{args.dataset}/gpe/{args.in_data_with_info}'
output_folder_path = f'{args.base_folder}/{args.dataset}/gpe/{args.out_candidates_folder_name}'
os.makedirs(output_folder_path, exist_ok=True)

country_lst, state_lst, city_lst = [], [], []

with open(in_data_with_info_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        for name, label in data['perturbable']:
            if label == 'country':
                country_lst.append(name)
            elif label == 'state':
                state_lst.append(name)
            elif label == 'city':
                city_lst.append(name)
            else:
                raise ValueError()
output_dict = {
    'country': country_lst,
    'state': state_lst,
    'city': city_lst,
}
with open(f'{output_folder_path}/candidate_names.json', 'w', encoding='utf-8') as f:
    json.dump(output_dict, f, indent=0, sort_keys=True)
