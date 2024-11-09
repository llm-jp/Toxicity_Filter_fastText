# pip install fugashi unidic-lite

import sys
import random
import json
import fugashi
import fasttext
import gzip

model = fasttext.load_model(sys.argv[1])
input_file = sys.argv[2]

tokenizer = fugashi.Tagger()


def tokenize_japanese_text(text):
    tokens = [word.surface for word in tokenizer(text)]
    return ' '.join(tokens)


with gzip.open(input_file) as f:
    for line in f:
        data = json.loads(line)
        text = data.get("text", "")
        if text:
            tokenized_text = tokenize_japanese_text(text)
            pred = model.predict(tokenized_text, k=2)
            d = dict(zip(pred[0], pred[1]))
            toxic_score = round(d['__label__toxic'], 4)
            print(toxic_score, flush=True)
