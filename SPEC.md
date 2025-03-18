# Nemulo 文法

ソースとなるテキストは、以下のような形式をとる:

```plaintext
filename:
summary:
category:

本文
```

## メタデータ

ファイル先頭から、最初の空行まではメタデータとして扱われる。メタデータの書式はPCREで表記すると以下の通りである:

```plaintext
(^¥w+):¥s+(.*)$
```

### filename

出力する html のファイル名。

### summary

ogp の description に埋め込む文章。

### category

現時点では使い道は決まっていない。

## 本文

Markdown に似ているが、実装していないもの、追加で実装しているもの、書き方が違うものがある。

### Markdown と同じもの

見出し

```plaintext
# 見出し (大; h3 に変換)
## 見出し (中; h4 に変換)
### 見出し (小; h5 に変換)
```

リンク

```plaintext
[text](url)
```

画像の貼り付け

```plaintext
![alt text](sample.jpg)
```

太字

```plaintext
**bold**
__bold__
```

`---` だけの行は水平線（`<hr>`）に変換される。

### Markdown と違うもの

#### 実装しないもの

* 斜体、斜体＋太字
* 箇条書き・リスト
* テーブル
* 参照
* コードブロック (```` ``` ````)

#### 改行

改行は `<br>` に変換される。

#### コメント

コメントは HTML と同じように書く。

```html
<!-- コメント -->
```

こうやって書かれたコメントは html に出力されない。

#### 省略

記事がトップページなど、複数の記事が掲載される html に出力されるとき、記事全体を掲載するには長すぎると考えられる場合は、本文中に以下のように書く。

```plaintext
:break
```

この場合、複数の記事を含む html ファイルでは `:break` の前の行までが使われる。この箇所に「続きを読む」といった、個別記事へのリンクを作る。

個別記事のファイルでは `:break` を取り除き、すべてを記載する。

#### 引用

引用したい文章を、`>>>` と `<<<` で囲む。これは `<blockquote>` タグに変換される。

引用元を示すときは、最後の行に `>` として、引用元の情報などを書く。この部分は右揃えになる。

クオートなどは自動では付与されない。引用元を示すときによく使う「ダッシュ」(`——`)も自動では付与されない。

```plaintext
>>>
“Democracy is the worst form of government, except for all those other forms that have been tried from time to time.”
> -- Winston S Churchill, 11 November 1947.
<<<
```

#### 目次

本文の先頭（メタデータの空行の直後）に `:toc` と書くと、目次が作られる。

```plaintext
:toc
```

#### 行の位置揃え

左揃え（標準）

```plaintext
:<
```

中央揃え

```plaintext
:=
```

右揃え

```plaintext
:>
```

#### 文字色と背景色

なんとなくおかしいかもしれないが、画像の貼り付けの `!` を `"` に変える、と考えると分かりやすい、かも。

```plaintext
"[text](front-color, back-color)`
```

`front-color` と `back-color` は `#FFFFFF` という16進数を取ることができる。

#### 傍点

Markdown だと「斜体＋太字」になる最上位の強調表示は、日本語だと傍点でしょう、ということで。

```plaintext
***傍点を付けたい文字列***
```

#### マーカー

日本語では斜体を使うシーンは限られているので、Markdown では斜体の文字修飾をするときはマーカーペンを使ったような表示をする。

ただ、マーカーペンにも種類があるのが問題…。

```plaintext
*markered_text*(marker_name)
```

`maerker_name` の種類:

* `yellow`, `green`, `pink`, `blue`
  * すべて蛍光マーカー
