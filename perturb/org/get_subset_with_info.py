import os
import json
import argparse

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--ptb_path', default='../nnp_dataset/ptb.txt')
parser.add_argument('--ptb_nnp_path', default='../nnp_dataset/ptb_nnp.txt')
parser.add_argument('--gpe_country_path', default='../gpe_dataset/countries.jsonl')
parser.add_argument('--gpe_state_path', default='../gpe_dataset/states.jsonl')
parser.add_argument('--gpe_city_path', default='../gpe_dataset/cities.jsonl')
parser.add_argument('--in_filename', default='dev_answer_entity.jsonl')
parser.add_argument('--out_filename', default='answer_entity_with_info.jsonl')

args = parser.parse_args()

in_path = f'{args.base_folder}/{args.dataset}/{args.in_filename}'
out_path = f'{args.base_folder}/{args.dataset}/org/{args.out_filename}'

os.makedirs(f'{args.base_folder}/{args.dataset}/org', exist_ok=True)
output_dict_lst = []


def read_word_set(txt_path):
    word_set = set()
    with open(txt_path, 'r') as f:
        for line in f:
            word = line.strip()
            word_set.add(word)
    return word_set


def read_word_dict(jsonl_path):
    word_dict = dict()
    with open(jsonl_path, 'r') as f:
        for line in f:
            name, lower_name = json.loads(line)
            if lower_name in word_dict:
                print(name, word_dict[lower_name])
            word_dict[lower_name] = name
    return word_dict


ptb_set = read_word_set(args.ptb_path)
ptb_nnp_set = read_word_set(args.ptb_nnp_path)
country_dict = read_word_dict(args.gpe_country_path)
state_dict = read_word_dict(args.gpe_state_path)
city_dict = read_word_dict(args.gpe_city_path)

with open(in_path, 'r', encoding="utf-8") as f_in:
    data_lst = [json.loads(line) for line in f_in]


def get_ngram_str_lst(word_lst):
    ngram_str_lst = []
    # from length to 2
    length = len(word_lst)
    for n in range(length, 1, -1):
        for i in range(length - n + 1):
            ngram_str_lst.append(' '.join(word_lst[i: i+n]))
    return ngram_str_lst


# find the perturbable words in the answers
for data in tqdm(data_lst):
    if 'ORG' in data['answer_entities']:
        org_lst = data['answer_entities']['ORG']
        output_dict = {'idx': data['idx'], 'orgs': org_lst, 'perturbable': []}
        detected_word_set = set()
        for org in org_lst:
            # priority: country > state > city > nnp > not_appear
            word_lst = org.split(' ')
            ngram_str_lst = get_ngram_str_lst(word_lst)
            for ngram_str in ngram_str_lst:
                # at least two words
                if ngram_str in country_dict:
                    ngram_word_set = set(ngram_str.split(' '))
                    if detected_word_set.isdisjoint(ngram_word_set):
                        output_dict['perturbable'].append((country_dict[ngram_str], 'country'))
                        detected_word_set |= ngram_word_set
                elif ngram_str in state_dict:
                    ngram_word_set = set(ngram_str.split(' '))
                    if detected_word_set.isdisjoint(ngram_word_set):
                        output_dict['perturbable'].append((state_dict[ngram_str], 'state'))
                        detected_word_set |= ngram_word_set
                elif ngram_str in city_dict:
                    ngram_word_set = set(ngram_str.split(' '))
                    if detected_word_set.isdisjoint(ngram_word_set):
                        output_dict['perturbable'].append((city_dict[ngram_str], 'city'))
                        detected_word_set |= ngram_word_set
            for word in word_lst:
                if word in country_dict and not (word in ptb_set and word not in ptb_nnp_set):  # avoid noise in the gpe data: e.g. "of" as a city name
                    if word not in detected_word_set:
                        output_dict['perturbable'].append((country_dict[word], 'country'))
                        detected_word_set.add(word)
                elif word in state_dict and not (word in ptb_set and word not in ptb_nnp_set):  # avoid noise in the gpe data: e.g. "of" as a city name
                    if word not in detected_word_set:
                        output_dict['perturbable'].append((state_dict[word], 'state'))
                        detected_word_set.add(word)
                elif word in city_dict and not (word in ptb_set and word not in ptb_nnp_set):  # avoid noise in the gpe data: e.g. "of" as a city name
                    if word not in detected_word_set:
                        output_dict['perturbable'].append((city_dict[word], 'city'))
                        detected_word_set.add(word)
                elif word in ptb_nnp_set:
                    if word not in detected_word_set:
                        output_dict['perturbable'].append((word, 'nnp'))
                        detected_word_set.add(word)
                elif word not in ptb_set:
                    if word not in detected_word_set:
                        output_dict['perturbable'].append((word, 'rare'))
                        detected_word_set.add(word)
        if len(detected_word_set):
            output_dict_lst.append(output_dict)

with open(out_path, 'w', encoding='utf-8') as f_out:
    for data in output_dict_lst:
        f_out.write(json.dumps(data) + '\n')
