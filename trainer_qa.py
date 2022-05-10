# coding=utf-8
# Copyright 2020 The HuggingFace Team All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
A subclass of `Trainer` specific to Question-Answering tasks
"""
import logging
import json

from transformers import Trainer, is_datasets_available, is_torch_tpu_available

from utils_qa import calc_score, output_pred

logger = logging.getLogger(__name__)

if is_datasets_available():
    import datasets

if is_torch_tpu_available():
    import torch_xla.core.xla_model as xm
    import torch_xla.debug.metrics as met


class QuestionAnsweringTrainer(Trainer):
    def __init__(self, *args, eval_examples=None, post_process_function=None, output_pred_path=None, output_metrics_only=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.eval_examples = eval_examples
        self.post_process_function = post_process_function
        self.output_pred_path = output_pred_path
        self.output_metrics_only = output_metrics_only

    def evaluate(self, eval_dataset=None, eval_examples=None, ignore_keys=None):
        eval_dataset = self.eval_dataset if eval_dataset is None else eval_dataset
        eval_dataloader = self.get_eval_dataloader(eval_dataset)
        eval_examples = self.eval_examples if eval_examples is None else eval_examples

        output = self.prediction_loop(
            eval_dataloader,
            description="Evaluation",
            prediction_loss_only=False,
            ignore_keys=ignore_keys,
        )

        # We might have removed columns from the dataset so we put them back.
        if isinstance(eval_dataset, datasets.Dataset):
            eval_dataset.set_format(type=eval_dataset.format["type"], columns=list(eval_dataset.features.keys()))

        if self.post_process_function is not None:
            eval_preds = self.post_process_function(eval_examples, eval_dataset, output.predictions)

            references = []
            predictions = []

            for pred, ref in zip(eval_preds.predictions, eval_preds.label_ids):
                predictions.append(pred['prediction_text'])
                references.append(ref['answers']['text'])

            aggregated_em, aggregated_f1, em_lst, f1_lst = calc_score(references, predictions)
            num_examples = len(em_lst)
            metrics = {'result': f'{aggregated_em*100:.2f}/{aggregated_f1*100:.2f}', 'eval_em': aggregated_em, 'eval_f1': aggregated_f1, 'eval_num_examples': num_examples}
            if self.output_pred_path:
                if self.output_metrics_only:
                    with open(self.output_pred_path, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(metrics) + '\n')
                else:
                    output_pred(predictions, references, em_lst, f1_lst, self.output_pred_path, metrics)

        if self.args.tpu_metrics_debug or self.args.debug:
            # tpu-comment: Logging debug metrics for PyTorch/XLA (compile, execute times, ops, etc.)
            xm.master_print(met.metrics_report())

        print(metrics)
        return metrics