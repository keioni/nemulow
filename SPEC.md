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

### 改行の扱い

Markdown と異なり、改行は `<br>` に変換される。

### コメント

コメントは HTML と同じように書く。

```html
<!-- コメント -->
```

こうやって書かれたコメントは html に出力されない。

### 省略

記事がトップページなど、複数の記事が掲載される html に出力されるとき、記事全体を掲載するには長すぎると考えられる場合は、本文中に以下のように書く。

```plaintext
:break
```

この場合、複数の記事を含む html ファイルでは `:break` の前の行までが使われる。この箇所に「続きを読む」といった、個別記事へのリンクを作る。

個別記事のファイルでは `:break` を取り除き、すべてを記載する。

### Markdown と同じもの

見出しや修飾には Markdown と同じものを使う。

#### 見出し

```plaintext
# 見出し (大; h3 に変換)
## 見出し (中; h4 に変換)
### 見出し (小; h5 に変換)
```

#### リンク

```plaintext
[text](url)
```

#### 画像

```plaintext
![alt text](sample.jpg)
```

#### 文字の修飾

```plaintext
*italic*
**bold**
***italic-bold***
_italic_
__bold__
___italic-bold___
```

#### インラインコード

バッククオートで囲むと `inline code` となる。

#### コードブロック

以下はコードブロックになる。

````plaintext
```
block code
```
````

#### 区切り線

`---` だけの行は水平線（`<hr>`）に変換される。

### Markdown との違い

#### 扱わないもの

* 箇条書き・リスト
* テーブル

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
