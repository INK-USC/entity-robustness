import json
import random
import os
import argparse

from faker import replace_in_doc_randstr, replace_in_doc_phrase, replace_in_doc_word, generate_randstr


parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--base_folder', default='../../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--in_full_data', default='dev.jsonl')
parser.add_argument('--in_data_with_info', default='answer_entity_with_info.jsonl')
parser.add_argument('--perturbation', default='none', choices=['none', 'RandStr', 'candidates'])
parser.add_argument('--candidates_folder_name', default='none', choices=['none', 'InDistName', 'EnName'])  # please ensure that it contains "candidate_names.json"

args = parser.parse_args()
assert (args.perturbation == 'candidates') + (args.candidates_folder_name == 'none') == 1

random.seed(args.seed)

in_full_data_path = f'{args.base_folder}/{args.dataset}/{args.in_full_data}'
in_data_with_info_path = f'{args.base_folder}/{args.dataset}/org/{args.in_data_with_info}'

idx2names = dict()
with open(in_data_with_info_path, 'r', encoding="utf-8") as f_in:
    for line in f_in:
        data = json.loads(line)
        idx2names[data['idx']] = data['perturbable']

subset_data_list = []
with open(in_full_data_path, 'r', encoding="utf-8") as f_in:
    for line in f_in:
        data = json.loads(line)
        idx = data['idx']
        if idx in idx2names:
            subset_data_list.append(data)

output_data_list = []


if args.perturbation == 'none':
    assert args.candidates_folder_name == 'none'
    output_data_list = subset_data_list
    out_path = f'{args.base_folder}/{args.dataset}/org/dev_subset.jsonl'
elif args.perturbation == 'RandStr':
    assert args.candidates_folder_name == 'none'
    for data in subset_data_list:
        idx = data['idx']
        name_lst = idx2names[idx]
        context = data["context"]
        question = data["question"]
        answers = data["answers"]["text"]
        for name, label in name_lst:
            for src_word in name.split(' '):
                tgt_word = generate_randstr(src_word)
                context = replace_in_doc_randstr(context, src_word, tgt_word)
                question = replace_in_doc_randstr(question, src_word, tgt_word)
                for ind, answer in enumerate(answers):
                    answers[ind] = replace_in_doc_randstr(answer, src_word, tgt_word)
        data["context"] = context
        data["question"] = question
        data["answers"]["text"] = answers
        output_data_list.append(data)
    os.makedirs(f'{args.base_folder}/{args.dataset}/org/RandStr', exist_ok=True)
    out_path = f'{args.base_folder}/{args.dataset}/org/RandStr/dev_subset_s{args.seed}.jsonl'
elif args.perturbation == 'candidates':
    assert args.candidates_folder_name != 'none'
    candidates_path = f'{args.base_folder}/{args.dataset}/org/{args.candidates_folder_name}/candidate_names.json'
    with open(candidates_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    country_lst, state_lst, city_lst = data['country'], data['state'], data['city']
    nnp_lst, rare_lst = data['nnp'], data['rare']
    for data in subset_data_list:
        idx = data['idx']
        name_lst = idx2names[idx]
        context = data["context"]
        question = data["question"]
        answers = data["answers"]["text"]
        phrase_mapping = []  # for country/state/city
        word_mapping = []  # for nnp/rare
        for src_name, label in name_lst:
            if label == 'country':
                if country_lst:
                    tgt_name = random.choice(country_lst)
                    phrase_mapping.append((src_name, tgt_name))
            elif label == 'state':
                if state_lst:
                    tgt_name = random.choice(state_lst)
                    phrase_mapping.append((src_name, tgt_name))
            elif label == 'city':
                if city_lst:
                    tgt_name = random.choice(city_lst)
                    phrase_mapping.append((src_name, tgt_name))
            elif label == 'nnp':
                if nnp_lst:
                    tgt_name = random.choice(nnp_lst)
                    word_mapping.append((src_name, tgt_name))
            elif label == 'rare':
                if rare_lst:
                    tgt_name = random.choice(rare_lst)
                    word_mapping.append((src_name, tgt_name))
            else:
                raise ValueError()
        for src_phrase, tgt_phrase in phrase_mapping:
            context = replace_in_doc_phrase(context, src_phrase, tgt_phrase)
            question = replace_in_doc_phrase(question, src_phrase, tgt_phrase)
            for ind, answer in enumerate(answers):
                answers[ind] = replace_in_doc_phrase(answer, src_phrase, tgt_phrase)
        for src_word, tgt_word in word_mapping:
            context = replace_in_doc_word(context, src_word, tgt_word)
            question = replace_in_doc_word(question, src_word, tgt_word)
            for ind, answer in enumerate(answers):
                answers[ind] = replace_in_doc_word(answer, src_word, tgt_word)
        data["context"] = context
        data["question"] = question
        data["answers"]["text"] = answers
        output_data_list.append(data)
    out_path = f'{args.base_folder}/{args.dataset}/org/{args.candidates_folder_name}/dev_subset_s{args.seed}.jsonl'
else:
    raise NotImplementedError()

with open(out_path, 'w', encoding='utf-8') as f:
    for data in output_data_list:
        f.write(json.dumps(data) + '\n')