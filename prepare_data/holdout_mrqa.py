import json
import random
import configargparse

parser = configargparse.ArgumentParser()
parser.add_argument('--input_folder', default='../data/MRQA')
parser.add_argument('--output_folder', default='../data')
parser.add_argument('--dataset_name', default='SQuAD', choices=['HotpotQA', 'NaturalQuestions', 'SearchQA', 'SQuAD', 'TriviaQA'])
parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--ratio', type=float, default=0.1)
args = parser.parse_args()

random.seed(args.seed)
print(args.dataset_name)
in_train_raw_jsonl = f'{args.input_folder}/train/{args.dataset_name}.jsonl'
in_train_processed_jsonl = f'{args.output_folder}/{args.dataset_name}/train.jsonl'
out_train_holdout_jsonl = f'{args.output_folder}/{args.dataset_name}/train_holdout.jsonl'
out_dev_holdout_jsonl = f'{args.output_folder}/{args.dataset_name}/dev_holdout.jsonl'
grouped_qid = []
qid_count = 0
with open(in_train_raw_jsonl, 'r', encoding='utf-8') as f:
    f.readline()
    for line in f:
        data = json.loads(line)
        qid_lst = [qas['qid'] for qas in data['qas']]
        qid_count += len(qid_lst)
        grouped_qid.append(qid_lst)
print(f'{qid_count} questions in {len(grouped_qid)} groups.')
sampled_grouped_qid = random.sample(grouped_qid, k=int(len(grouped_qid) * args.ratio))
sampled_qid_lst = sum(sampled_grouped_qid, [])
sampled_qid_set = set(sampled_qid_lst)
with open(in_train_processed_jsonl, 'r', encoding='utf-8') as f_in, \
        open(out_train_holdout_jsonl, 'w', encoding='utf-8') as f_out_train, \
        open(out_dev_holdout_jsonl, 'w', encoding='utf-8') as f_out_dev:
    train_count = 0
    dev_count = 0
    for line in f_in:
        data = json.loads(line)
        if data['id'] in sampled_qid_set:
            f_out_dev.write(line)
            dev_count += 1
        else:
            f_out_train.write(line)
            train_count += 1
    print('train', train_count)
    print('dev', dev_count)
