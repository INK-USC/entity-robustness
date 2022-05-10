import json
import random
import os
import argparse

from faker import replace_in_doc, generate_randstr


parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--base_folder', default='../../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--in_full_data', default='dev.jsonl')
parser.add_argument('--in_data_with_info', default='answer_entity_with_info.jsonl')
parser.add_argument('--perturbation', default='none', choices=['none', 'RandStr', 'candidates'])
parser.add_argument('--candidates_folder_name', default='none', choices=['none', 'InDistName', 'EnName', 'ChineseName',
                                                                         'ArabicName', 'FrenchName', 'IndianName'])  # please ensure that it contains "candidate_names.json"

args = parser.parse_args()
assert (args.perturbation == 'candidates') + (args.candidates_folder_name == 'none') == 1

random.seed(args.seed)

in_full_data_path = f'{args.base_folder}/{args.dataset}/{args.in_full_data}'
in_data_with_info_path = f'{args.base_folder}/{args.dataset}/person/{args.in_data_with_info}'

idx2names = dict()
with open(in_data_with_info_path, 'r', encoding="utf-8") as f_in:
    for line in f_in:
        data = json.loads(line)
        idx2names[data['idx']] = data['names']

subset_data_list = []
with open(in_full_data_path, 'r', encoding="utf-8") as f_in:
    for line in f_in:
        data = json.loads(line)
        idx = data['idx']
        if idx in idx2names:
            subset_data_list.append(data)

output_data_list = []


def read_candidates(candidate_names_path):
    with open(candidate_names_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    male_first_name_lst = data['first_name_male']
    female_first_name_lst = data['first_name_female']
    neutral_first_name_lst = data['first_name_neutral']
    last_name_lst = data['last_name']
    return male_first_name_lst, female_first_name_lst, neutral_first_name_lst, last_name_lst


# {"idx": 0,
#  "context": "[INK] [INK] Hold On to the Nights\"Hold On to the Nights\" is a power ballad and number-one hit for American rock singer/songwriter/musician Richard Marx.  This was the fourth and final single released from his self-titled debut album, and the first to reach the top of the Billboard Hot 100 chart. [INK] Written by Richard Marx, \"Hold On to the Nights\" reached the Billboard Hot 100 number 1 position on July 23, 1988, preventing Def Leppard's \"Pour Some Sugar On Me\" from reaching the top spot that same week. The song was on the chart for twenty-one weeks, and left the chart at number 65. From Marx' debut 1987 album, Richard Marx, the song also reached number three on the Billboard Adult Contemporary chart. \"Hold On to the Nights\" has been re-released numerous albums  and is included on Marx's live performance DVD A Night Out with Friends (2012). [INK] Charts",
#  "question": "Who had an 80s No 1 hit with Hold On To The Nights?",
#  "id": "feabd1ae0c0246699a00e4e4b84cae69",
#  "detected_answers": {"answer_start": [139, 620, 314], "text": ["richard marx", "richard marx", "richard marx"]},
#  "answers": {"text": ["richard marx"]}}


if args.perturbation == 'none':
    assert args.candidates_folder_name == 'none'
    output_data_list = subset_data_list
    out_path = f'{args.base_folder}/{args.dataset}/person/dev_subset.jsonl'
elif args.perturbation == 'RandStr':
    assert args.candidates_folder_name == 'none'
    for data in subset_data_list:
        idx = data['idx']
        name_lst = idx2names[idx]
        context = data["context"]
        question = data["question"]
        answers = data["answers"]["text"]
        for name_with_info in name_lst:
            word_lst = name_with_info[1:]  # gender excluded
            for src_word_lower in word_lst:
                tgt_word = generate_randstr(src_word_lower)
                context = replace_in_doc(context, src_word_lower, tgt_word)
                question = replace_in_doc(question, src_word_lower, tgt_word)
                for ind, answer in enumerate(answers):
                    answers[ind] = replace_in_doc(answer, src_word_lower, tgt_word)
        data["context"] = context
        data["question"] = question
        data["answers"]["text"] = answers
        output_data_list.append(data)
    os.makedirs(f'{args.base_folder}/{args.dataset}/person/RandStr', exist_ok=True)
    out_path = f'{args.base_folder}/{args.dataset}/person/RandStr/dev_subset_s{args.seed}.jsonl'
elif args.perturbation == 'candidates':
    assert args.candidates_folder_name != 'none'
    candidates_path = f'{args.base_folder}/{args.dataset}/person/{args.candidates_folder_name}/candidate_names.json'
    male_first_name_lst, female_first_name_lst, neutral_first_name_lst, last_name_lst = read_candidates(candidates_path)
    for data in subset_data_list:
        idx = data['idx']
        name_lst = idx2names[idx]
        context = data["context"]
        question = data["question"]
        answers = data["answers"]["text"]
        for name_with_info in name_lst:
            gender = name_with_info[0]
            word_lst = name_with_info[1:]
            if len(word_lst) == 1:
                original_first_name, = word_lst
                if gender == 'M':
                    pool = male_first_name_lst
                elif gender == 'F':
                    pool = female_first_name_lst
                else:
                    pool = neutral_first_name_lst
                new_first_name = random.choice(pool)
                mapping = [(original_first_name, new_first_name)]
            elif len(word_lst) == 2:
                original_first_name, original_last_name = word_lst
                if gender == 'M':
                    first_name_pool = male_first_name_lst
                elif gender == 'F':
                    first_name_pool = female_first_name_lst
                else:
                    first_name_pool = neutral_first_name_lst
                last_name_pool = last_name_lst
                new_first_name = random.choice(first_name_pool)
                new_last_name = random.choice(last_name_pool)
                mapping = [(original_first_name, new_first_name), (original_last_name, new_last_name)]
            else:
                raise ValueError()
            for src_word_lower, tgt_word in mapping:
                context = replace_in_doc(context, src_word_lower, tgt_word)
                question = replace_in_doc(question, src_word_lower, tgt_word)
                for ind, answer in enumerate(answers):
                    answers[ind] = replace_in_doc(answer, src_word_lower, tgt_word)
        data["context"] = context
        data["question"] = question
        data["answers"]["text"] = answers
        output_data_list.append(data)
    out_path = f'{args.base_folder}/{args.dataset}/person/{args.candidates_folder_name}/dev_subset_s{args.seed}.jsonl'
else:
    raise NotImplementedError()


with open(out_path, 'w', encoding='utf-8') as f:
    for data in output_data_list:
        f.write(json.dumps(data) + '\n')

