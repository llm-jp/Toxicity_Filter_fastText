# 有害文書フィルタリング

## 準備

- `/path/to/ja_cc/`にフィルタリング対象のファイル`CC-MAIN-2013-2016.jsonl.gz`、`CC-MAIN-2017-04.jsonl.gz`などがあるとします。
- `ft_model.bin` ... フィルタリングに使うfastTextモデルです。
- `predict_ja_cc_gz.py` ... モデルとフィルタリング対象のファイルを読み込んで、ファイル中の各`text`の有害スコアを計算します。
- `do_filter.py` ... 有害スコアに基づいて`text`をフィルタリング（有害か無害かに分類）します。

## 手順

まず`CC-MAIN-2013-2016.jsonl.gz`、`CC-MAIN-2017-04.jsonl.gz`などのファイルのリスト`file_list`を作り、ファイルごとに、そのファイル中の各`text`に対する有害スコアを計算します。
`GNU parallel`で並列実行します。

```
ls /path/to/ja_cc/ | sed 's/\.gz//' > file_list

mkdir toxic_scores/

parallel -j 30 'python3 predict_ja_cc_gz.py \
    ft_model.bin /path/to/ja_cc/{}.gz > toxic_scores/{.} ' \
    :::: file_list
```

上記の結果、`toxic_scores/`に、`CC-MAIN-2013-2016.jsonl.gz`、`CC-MAIN-2017-04.jsonl.gz`などのファイルにある各`text`に対する有害スコアが出力されます。例えば`CC-MAIN-2013-2016.jsonl.gz`の有害スコアは`toxic_scores/CC-MAIN-2013-2016`に出力されます。一行につき１つの`text`に対する有害スコアが記載されます。上記の処理で、だいたい3時間から6時間くらいかかるかもしれません。

次に、有害スコアに基づいて各`text`をフィルタリング（有害か無害かに分類）します。

```
mkdir ja_cc_toxic ja_cc_toxicity_filtered

python3 do_filter.py /path/to/ja_cc/ toxic_scores/ ja_cc_toxic/ ja_cc_toxicity_filtered/
```

`ja_cc_toxic/`に有害な`text`が、`ja_cc_toxicity_filtered/`に無害な`text`が出力されます。`do_filter.py`に`threshold = 0.99`とありますが、この`0.99`が分類閾値です。

