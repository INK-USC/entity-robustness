import json
from shutil import copyfile

# confirm that one instance of SQuAD is the only instance that is affected
# long_space = ' ' * 500
# dataset_lst = ['HotpotQA', 'NaturalQuestions', 'SearchQA', 'SQuAD', 'TriviaQA']
# for dataset in dataset_lst:
#     for split in ['train', 'dev']:
#         jsonl_path = f'../data/{dataset}/{split}.jsonl'
#         with open(jsonl_path, 'r', encoding='utf-8') as f:
#             for idx, line in enumerate(f):
#                 data = json.loads(line)
#                 context = data['context']
#                 question = data['question']
#                 if long_space in context:
#                     print(jsonl_path)
#                     print(idx)
#                     print(context)
#                 if long_space in question:
#                     print(jsonl_path)
#                     print(idx)
#                     print(question)

# output
# ../data/SQuAD/train.jsonl
# 74851

target_path = '../data/SQuAD/train.jsonl'
tgt_idx = 74851
copyfile(target_path, f'{target_path}.bak')
with open(target_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
tgt_line = lines[tgt_idx]
tgt_data = json.loads(tgt_line)
tgt_data['question'] = tgt_data['question'].strip()
lines[tgt_idx] = json.dumps(tgt_data) + '\n'
with open(target_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
