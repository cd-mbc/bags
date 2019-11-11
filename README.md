

# Bags Command 


## Prerequisite

- python2
- rosbag API for python: http://wiki.ros.org/rosbag/Code%20API


ソースのダウンロード, 環境変数の設定, aliasの設定.

```
git clone https://github.com/cd-mbc/bags
cd ./bags
export BAGSPATH=$PWD
alias bags='python $BAGSPATH/src/bags.py'
```

## Usage

```
bags -d <directory> {meta, data, info}
```

directoryには, bagファイルを探索する際のルートディレクトリを指定することができる. ここで指定したディレクトリから再帰的にそのサブディレクトリを全て探索する. デフォルトはカレントディレクトリ.

### meta

```
bags -d <directory> meta -f <filter>
```

filterには, bagファイルの検索条件として, python の真偽式を指定することができる.  
また, 以下の追加の変数が利用可能. 基本的に rosbag python API で取得できるメタ情報をそのまま利用, もしくは一部修正したもの.

- start
    - BagTime
        - floatを拡張したクラスで, 値としてunix time, 追加のattributeとしてdatetime (datetime型)を保持している.
    - 記録開始時刻
- end = BagTime
    - BagTime
    - 記録終了時刻
- comp
    - CompressionTuple:
        - compression: 圧縮バージョン (str)
        - uncompressed: 圧縮されていないデータサイズ (float)
        - compressed: 圧縮されているデータサイズ (float)
    - ファイルの圧縮に関する情報. compressionはバージョン2.0ではnoneまたはbz2.  
      圧縮されていない場合は, uncompressedとcompressedは同一の値.
- count
    - int
    - ファイルに記録されたメッセージの総数
- size
    - float
    - ファイルサイズ
- ver 
    - int
    - bagファイル形式のバージョン (e.g., 2.0なら200)
- path
    - str
    - ファイル名
- types
    - 辞書
        - key: メッセージ型名 (str)
        - value: MD5ハッシュ (str)
    - ファイルに含まれるメッセージの型
- topics
    - 辞書
        - key: トピック名 (str)
        - value: TopicTuple
            - msg_type: メッセージ型 (str)
            - message_count: メッセージ数 (int)
            - connections: コネクションの数 (int)
            - frequency: データのレート (float)
    - ファイルに含まれるメッセージのトピック情報

#### 実行例

記録期間が10秒以上のファイルを検索.
```
bags meta -d . -f 'end - start >= 10'
```

### data

```
bags data <topic> -f <filter>
```

指定されたトピックについて, 条件を満たすメッセージを含むファイルを出力する. フィルターにはpythonの真偽式を指定し, 以下の変数が利用可能. 

- msg
    - 各トピックごとに定義される各メッセージのクラス (infoコマンドで詳細は確認可能)
    - メッセージデータ


### info

```
bags info --topic <topic> 
```

指定されたトピックを含むファイルに含まれる最初のメッセージをサンプルとして出力する. これを使ってmsgの構造について確認することができる. また, 特定のトピックについて定義されている拡張メソッドの情報についても表示する. 

## 各環境変数について

- BAGSNUMPROC
    - 利用可能な最大プロセス数を指定
    - 検索対象となるファイルを指定された数のプロセスに割り当てることで処理を高速化する

- BAGSFILEASSIGN
    - 複数プロセスに対して処理するファイルを割り当てる方法を指定
    - 0を指定するとファイルを見つけた順で割り当て
    - 1を指定するとファイルサイズでソートしたのち順に割り当てる

- BAGSDEBUG
    - Trueを指定すると, 各デバッグメッセージを出力する

- BAGSLIMITED
    - Falseにした場合, 検索条件として指定するフィルターには任意のpythonコードを指定することができる.
    - Trueの場合, フィルターに指定したコードから生成されるAST aには以下の制限が与えられる.
        - 1文で表現される式に限る.
        ```
        len(a.body) == 1
        ```

        - 文はast.Exprに限る.
        ```
        a.body[0].__class__ == ast.Expr
        ```

        - 使用可能なidentifierは以下に含まれるものに限る.
        ```
        selfdef_ids = ['start','end','comp','count','count','size','ver','path','types','topics','msg']
        predef_ids = ['True','False','type','int','str','float','double']
        ```



