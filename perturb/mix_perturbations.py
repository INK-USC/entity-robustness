import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--ent_type_lst', nargs='+', default=['person', 'org', 'gpe'])
parser.add_argument('--perturbation', default='InDistName')
parser.add_argument('--seed', type=int, default=0)
args = parser.parse_args()


def merge_jsonl_lst(jsonl_path_lst, output_jsonl_path):
    idx_set = set()
    output_data_lst = []
    for jsonl_path in jsonl_path_lst:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data['idx'] not in idx_set:
                    idx_set.add(data['idx'])
                    output_data_lst.append(data)
    output_data_lst = sorted(output_data_lst, key=lambda x: x['idx'])
    with open(output_jsonl_path, 'w', encoding='utf-8') as f:
        for data in output_data_lst:
            f.write(json.dumps(data) + '\n')


os.makedirs(f'{args.base_folder}/{args.dataset}/mix', exist_ok=True)
for filename in ['answer_entity_with_info.jsonl', 'dev_subset.jsonl']:
    output_jsonl_path = f'{args.base_folder}/{args.dataset}/mix/{filename}'
    if not os.path.exists(output_jsonl_path):
        jsonl_path_lst = [f'{args.base_folder}/{args.dataset}/{ent_type}/{filename}' for ent_type in args.ent_type_lst]
        merge_jsonl_lst(jsonl_path_lst, output_jsonl_path)

os.makedirs(f'{args.base_folder}/{args.dataset}/mix/{args.perturbation}', exist_ok=True)
filename = f'dev_subset_s{args.seed}.jsonl'
jsonl_path_lst = [f'{args.base_folder}/{args.dataset}/{ent_type}/{args.perturbation}/{filename}' for ent_type in args.ent_type_lst]
output_jsonl_path = f'{args.base_folder}/{args.dataset}/mix/{args.perturbation}/{filename}'
merge_jsonl_lst(jsonl_path_lst, output_jsonl_path)
