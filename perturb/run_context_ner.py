import json

import argparse
import spacy
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', default='../data')
parser.add_argument('--dataset', default='SQuAD')
parser.add_argument('--in_filename', default='dev.jsonl')
parser.add_argument('--out_filename', default='dev_context_ner.jsonl')  # ner results for each instance

args = parser.parse_args()

in_path = f'{args.base_folder}/{args.dataset}/{args.in_filename}'
out_path = f'{args.base_folder}/{args.dataset}/{args.out_filename}'

nlp = spacy.load("en_core_web_sm")

with open(in_path, 'r', encoding="utf-8") as f_in:
    lines = f_in.readlines()
with open(out_path, 'w', encoding="utf-8") as f_out:
    for line in tqdm(lines):
        data = json.loads(line)
        idx = data['idx']
        context = data["context"]
        doc = nlp(context)
        output_lst = []
        for entity in doc.ents:
            text = entity.text
            label = entity.label_
            span = (entity.start_char, entity.end_char)
            triple = (text, label, span)
            output_lst.append(triple)
        output_dict = {
            'idx': idx,
            'entities': output_lst
        }
        f_out.write(json.dumps(output_dict) + '\n')
