mkdir -p ../data/MRQA/train/
mkdir -p ../data/MRQA/in_domain_dev/

wget -P ../data/MRQA/train/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/SQuAD.jsonl.gz
wget -P ../data/MRQA/train/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/NaturalQuestionsShort.jsonl.gz
wget -P ../data/MRQA/train/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/HotpotQA.jsonl.gz
wget -P ../data/MRQA/train/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/SearchQA.jsonl.gz
wget -P ../data/MRQA/train/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/TriviaQA-web.jsonl.gz

wget -P ../data/MRQA/in_domain_dev/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/SQuAD.jsonl.gz
wget -P ../data/MRQA/in_domain_dev/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/NaturalQuestionsShort.jsonl.gz
wget -P ../data/MRQA/in_domain_dev/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/HotpotQA.jsonl.gz
wget -P ../data/MRQA/in_domain_dev/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/SearchQA.jsonl.gz
wget -P ../data/MRQA/in_domain_dev/ https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/TriviaQA-web.jsonl.gz

gunzip ../data/MRQA/train/SQuAD.jsonl.gz
gunzip ../data/MRQA/train/NaturalQuestionsShort.jsonl.gz
gunzip ../data/MRQA/train/HotpotQA.jsonl.gz
gunzip ../data/MRQA/train/SearchQA.jsonl.gz
gunzip ../data/MRQA/train/TriviaQA-web.jsonl.gz

gunzip ../data/MRQA/in_domain_dev/SQuAD.jsonl.gz
gunzip ../data/MRQA/in_domain_dev/NaturalQuestionsShort.jsonl.gz
gunzip ../data/MRQA/in_domain_dev/HotpotQA.jsonl.gz
gunzip ../data/MRQA/in_domain_dev/SearchQA.jsonl.gz
gunzip ../data/MRQA/in_domain_dev/TriviaQA-web.jsonl.gz

mv ../data/MRQA/train/TriviaQA-web.jsonl ../data/MRQA/train/TriviaQA.jsonl
mv ../data/MRQA/in_domain_dev/TriviaQA-web.jsonl ../data/MRQA/in_domain_dev/TriviaQA.jsonl
mv ../data/MRQA/train/NaturalQuestionsShort.jsonl ../data/MRQA/train/NaturalQuestions.jsonl
mv ../data/MRQA/in_domain_dev/NaturalQuestionsShort.jsonl ../data/MRQA/in_domain_dev/NaturalQuestions.jsonl
