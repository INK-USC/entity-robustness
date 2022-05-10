import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../../../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--out_candidates_folder_name', default='EnName')
parser.add_argument('--country_path', default='../../gpe_dataset/countries.jsonl')
parser.add_argument('--state_path', default='../../gpe_dataset/states.jsonl')
parser.add_argument('--city_path', default='../../gpe_dataset/cities.jsonl')
parser.add_argument('--nnp_path', default='../../nnp_dataset/ptb_nnp.txt')

args = parser.parse_args()


output_folder_path = f'{args.base_folder}/{args.dataset}/gpe/{args.out_candidates_folder_name}'
os.makedirs(output_folder_path, exist_ok=True)

with open(args.country_path, 'r', encoding='utf-8') as f:
    country_lst = [json.loads(line)[0] for line in f]
with open(args.state_path, 'r', encoding='utf-8') as f:
    state_lst = [json.loads(line)[0] for line in f]
with open(args.city_path, 'r', encoding='utf-8') as f:
    city_lst = [json.loads(line)[0] for line in f]

output_dict = {
    'country': country_lst,
    'state': state_lst,
    'city': city_lst,
}
with open(f'{output_folder_path}/candidate_names.json', 'w', encoding='utf-8') as f:
    json.dump(output_dict, f, indent=0, sort_keys=True)
