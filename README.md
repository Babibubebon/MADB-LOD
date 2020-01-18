MADB-LOD
=====
[メディア芸術データベース](https://mediaarts-db.bunka.go.jp/) Web APIからデータを取得するためのクローラと、RDFへの変換スクリプト

## Usage
依存パッケージのインストール
```
$ pip install -r requirements.txt
```

### メディア芸術データベース Web APIからデータ取得
```
$ scrapy crawl api [-a fieldId={animation,collection,game,manga,mediaart}]
```

取得したデータは分野ごとにJSON Lines形式で出力されます。
- `{animation,collection,game,manga,mediaart}.jsonl`

#### 設定ファイル(`madb/settings.py`)について
- 全件取得はかなりサーバ負荷をかけていると思われるので、不用意に`DOWNLOAD_DELAY`を小さくしないようご注意ください。

### RDFへ変換
```
$ ./convert_to_rdf.py *.jsonl
```

変換結果はN-Triples形式で `madb.nt` ファイルに出力されます。

RDF語彙へのマッピングは、QName-likeなWeb APIレスポンス「メタデータキー名」からお気持ちを汲んで設定しました。([Web APIドキュメント](https://mediaarts-db.bunka.go.jp/resources/pdf/mediaartsdb_webapi_documents.pdf)を参照)