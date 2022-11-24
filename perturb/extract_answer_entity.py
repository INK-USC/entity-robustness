import json
from collections import defaultdict

import argparse
from tqdm import tqdm

from common import normalize_entity_name

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--in_data_filename', default='dev.jsonl')
parser.add_argument('--in_ner_filename', default='dev_context_ner.jsonl')
parser.add_argument('--out_filename', default='dev_answer_entity.jsonl')

args = parser.parse_args()

in_data_path = f'{args.base_folder}/{args.dataset}/{args.in_data_filename}'
in_ner_path = f'{args.base_folder}/{args.dataset}/{args.in_ner_filename}'
out_path = f'{args.base_folder}/{args.dataset}/{args.out_filename}'

answer_entity_vocab = dict()
with open(in_data_path, 'r', encoding="utf-8") as f_in:
    data_lines = [json.loads(line) for line in f_in.readlines()]
with open(in_ner_path, 'r', encoding="utf-8") as f_in:
    ner_lines = [json.loads(line) for line in f_in.readlines()]
assert [line['idx'] for line in data_lines] == [line['idx'] for line in ner_lines]


def filter_entity_lst(entity_lst):
    # ensure that the detected entities within each type have no word overlapping
    output_lst = []
    output_word_set = set()
    # if len(entity_lst) > 1:
    #     print()
    for entity_name in sorted(entity_lst, key=lambda x: len(x.split(' ')), reverse=True):
        if any([entity_name in existing_entity for existing_entity in output_lst]):
            continue
        entity_word_set = set(entity_name.split(' '))
        if len(output_word_set & entity_word_set) == 0:
            output_lst.append(entity_name)
            output_word_set |= entity_word_set
    # if len(output_lst) > 1:
    #     print()
    return output_lst


output_dict_lst = []
for data_line, ner_line in zip(tqdm(data_lines), ner_lines):
    idx = data_line['idx']
    answers = data_line['answers']['text']
    answer_entities = defaultdict(list)
    for answer in set(answers):
        answer = answer.lower()
        entity_set = {(normalize_entity_name(entity_name, entity_type), entity_type) for entity_name, entity_type, _ in ner_line['entities']}
        for entity_name, entity_type in entity_set:
            if entity_name in answer:
                if all([name_with_space not in f' {answer} ' for name_with_space in [f' {entity_name} ',
                                                                                     f'"{entity_name} ',
                                                                                     f' {entity_name}"',
                                                                                     f'"{entity_name}"',
                                                                                     f' {entity_name}\'',
                                                                                     f'\'{entity_name}\'',
                                                                                     f'"{entity_name}:',
                                                                                     f' {entity_name},',
                                                                                     ]]):
                    print(f'Normalized entity name: {entity_name}')
                    print(f'Answer: {answer}')
                    print()
                    continue
                answer_entities[entity_type].append(entity_name)
    for entity_type, entity_lst in answer_entities.items():
        answer_entities[entity_type] = filter_entity_lst(entity_lst)
    output_dict = {'idx': idx, 'answer_entities': answer_entities}
    output_dict_lst.append(output_dict)

with open(out_path, 'w', encoding='utf-8') as f_out:
    for output_dict in output_dict_lst:
        f_out.write(json.dumps(output_dict) + '\n')
