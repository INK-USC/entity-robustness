# On the Robustness of Reading Comprehension Models to Entity Renaming

This repo contains the code for paper [*On the Robustness of Reading Comprehension Models to Entity Renaming*](https://arxiv.org/abs/2110.08555), accepted to *NAACL 2022*.

# 1. Preparation

## 1.1. Dependencies

```bash
conda create -n robustness python=3.7
conda activate robustness
conda install pytorch==1.7.1 -c pytorch
pip install transformers==4.10.2
pip install sentencepiece
pip install datasets==1.11.0
pip install spacy==3.1.2 
python -m spacy download en_core_web_sm
```

## 1.2. Prepare MRC Datasets

Go to `./prepare_data/`.
```bash
bash download.sh
python preprocess_mrqa.py
python fix_mrqa_squad.py
python holdout_mrqa.py
```

The MRC datasets will be prepared under `./data/`.

Note that the new `train`/`dev`/`test` sets will be named as `train_holdout.jsonl`/`dev_holdout.jsonl`/`dev.jsonl` respectively.

# 2. Generate Perturbed Test Sets for `<DATASET>`

> `<DATASET>`: chosen from [`SQuAD`, `NaturalQuestions`, `HotpotQA`, `SearchQA`, `TriviaQA`].

## 2.1. Answer Entity Recognition

Go to `./perturb/`.
```bash
python run_context_ner.py --dataset <DATASET>
python extract_answer_entity.py --dataset <DATASET>
```

## 2.2. Perturbable Span Identification for `<ENTITY_TYPE>`

> `<ENTITY_TYPE>`: chosen from [`person`, `org`, `gpe`].

Go to `./perturb/<ENTITY_TYPE>/`.
```bash
python get_subset_with_info.py --dataset <DATASET>
```

## 2.3. Candidate Name Sampling + Name Substitution for `<ENTITY_TYPE>`

- Original (a subset on which the perturbation for `<ENTITY_TYPE>` is applicable)
   
   Go to `./perturb/<ENTITY_TYPE>/`.
   ```bash
   python perturb.py --dataset <DATASET> --perturbation none
   ```
   
- RandStr
   
   Go to `./perturb/<ENTITY_TYPE>/`.
   ```bash
   python perturb.py --dataset <DATASET> --perturbation RandStr --seed <SAMPLING_SEED>
   ```
   > `<SAMPLING_SEED>`: an `int` for specifying the random seed in sampling. 

- InDistName and DBName
   
   1. Sample Candidate Names from `<CANDIDATE_SOURCE>`
      > `<CANDIDATE_SOURCE>` for person: chosen from [`InDistName`, `EnName`, `ChineseName`, `ArabicName`, `FrenchName`, `IndianName`].
      > 
      > `<CANDIDATE_SOURCE>` for org and gpe: chosen from [`InDistName`, `EnName`].

      Go to `./perturb/<ENTITY_TYPE>/<CANDIDATE_SOURCE>/`.
      ```bash
      python prepare_candidates.py --dataset <DATASET>
      ```
   
   2. Substitute with Candidate Names from `<CANDIDATE_SOURCE>`
   
      Go to `./perturb/<ENTITY_TYPE>/`.
      ```bash
      python perturb.py --dataset <DATASET> --perturbation candidates --candidates_folder_name <CANDIDATE_SOURCE> --seed <SAMPLING_SEED>
      ```
   
# 3. Model Training

Go to `./`.

```bash
python run_qa.py config/mrqa.json \
  --model_name_or_path <MODEL_FULL_NAME> \
  --train_jsonl data/<DATASET>/train_holdout.jsonl \
  --eval_jsonl data/<DATASET>/dev_holdout.jsonl \
  --output_dir models/<DATASET>/<MODEL_SAVE_NAME>_s<TRAINING_SEED> \
  --output_pred_path models/<DATASET>/<MODEL_SAVE_NAME>_s<TRAINING_SEED>/dev_holdout_pred.jsonl \
  --seed <TRAINING_SEED>
```
> `<MODEL_FULL_NAME>`: chosen from [`bert-base-cased`, `roberta-base`, `SpanBERT/spanbert-base-cased`].
> 
> `<DATASET>`: chosen from [`SQuAD`, `NaturalQuestions`, `HotpotQA`, `SearchQA`, `TriviaQA`].
> 
> `<MODEL_SAVE_NAME>`: a `str` for naming the folder to store the training checkpoints.
> 
> `<TRAINING_SEED>`: an `int` for specifying the random seed in training. 

# 4. Model Evaluation

Go to `./`.

```bash
python run_qa.py config/mrqa_eval.json \
  --model_name_or_path models/<DATASET>/<MODEL_SAVE_NAME>_s<TRAINING_SEED> \
  --eval_jsonl <EVAL_JSONL_PATH> \
  --output_pred_path <OUTPUT_PRED_PATH>
```
> `<EVAL_JSONL_PATH>`: a `str` for specifying the path for the original or perturbed test sets.
> 
>  > Path for the original test set: `./data/<DATASET>/<ENTITY_TYPE>/dev_subset.jsonl`.
>  >
>  > Path for the perturbed test set: `./data/<DATASET>/<ENTITY_TYPE>/<CANDIDATE_SOURCE>/dev_subset_s<SAMPLING_SEED>.jsonl`
> 
> `<OUTPUT_PRED_PATH>`: a `str` for specifying the path to save model predictions.

## Citation

```bibtex
@inproceedings{yan-etal-2022-robustness,
    title = "On the Robustness of Reading Comprehension Models to Entity Renaming",
    author = "Yan, Jun and Xiao, Yang and Mukherjee, Sagnik and Lin, Bill Yuchen and Jia, Robin and Ren, Xiang",
    booktitle = "Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
    month = jul,
    year = "2022",
    address = "Seattle, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.naacl-main.37",
    doi = "10.18653/v1/2022.naacl-main.37",
    pages = "508--520",
}
```