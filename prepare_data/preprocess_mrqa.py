import json
import os

input_folder = '../data/MRQA'
output_folder = '../data'
dataset_name_lst = ['HotpotQA', 'NaturalQuestions', 'SearchQA', 'SQuAD', 'TriviaQA']


def normalize_context(s):
    for mrqa_sep in ['[SEP]', '[TLE]', '[DOC]', '[PAR]']:
        s = s.replace(mrqa_sep, '[INK]')
    return s


def process_data(in_jsonl_path, out_jsonl_path):
    print(in_jsonl_path)
    out_data = []
    idx = 0
    instance_with_multi_answers = 0
    instance_in_dataset = 0
    with open(in_jsonl_path, 'r', encoding='utf-8') as f:
        f.readline()
        for line in f:
            data = json.loads(line)
            context = normalize_context(data['context'])
            for qas in data['qas']:
                qid = qas['qid']
                question = qas['question']
                detected_answers = qas['detected_answers']
                answers = qas['answers']
                out_dict = {
                    'idx': idx,
                    'context': context,
                    'question': question,
                    'id': qid,
                    'detected_answers': {'answer_start': [], 'text': []},
                    'answers': {'text': answers}
                }
                instance_in_dataset += 1
                if len(detected_answers) > 1:
                    instance_with_multi_answers += 1
                    if 'train' in in_jsonl_path:
                        continue
                for detected_ans in detected_answers:
                    answer_text = detected_ans['text']
                    for answer_char_span in detected_ans['char_spans']:
                        out_dict['detected_answers']['text'].append(answer_text)
                        out_dict['detected_answers']['answer_start'].append(answer_char_span[0])
                out_data.append(out_dict)
                idx += 1
    print(f'{instance_with_multi_answers}/{instance_in_dataset} instances have multiple answer spans')
    print(f'{len(out_data)} instances output.')
    with open(out_jsonl_path, 'w', encoding='utf-8') as f:
        for data in out_data:
            f.write(json.dumps(data) + '\n')


for dataset_name in dataset_name_lst:
    print(dataset_name)
    train_in_jsonl = f'{input_folder}/train/{dataset_name}.jsonl'
    dev_in_jsonl = f'{input_folder}/in_domain_dev/{dataset_name}.jsonl'
    os.makedirs(f'{output_folder}/{dataset_name}', exist_ok=True)
    train_out_jsonl = f'{output_folder}/{dataset_name}/train.jsonl'
    dev_out_jsonl = f'{output_folder}/{dataset_name}/dev.jsonl'
    process_data(train_in_jsonl, train_out_jsonl)
    process_data(dev_in_jsonl, dev_out_jsonl)
