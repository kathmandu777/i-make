# Diagnosis Mode

診断に使用するデータを格納

## Data Structure

```yaml
"質問(Node)のID":
    category: "質問のカテゴリ(質問が一つの場合は省略可能)"
    answers:
        blue_base:
            label: ブルベ(表示させる質問のラベル)
            next_node_id: 次の質問(Node)のID
            settings: {}
        yellow_base:
            label: イエベ
            next_node_id: 次の質問(Node)のID
            settings:
                glitter: imake/static/modes/custom/glitter/glitterS.png
                glitter-color: # パーツの色を設定するときは、`パーツ名-color`というキーで設定する
                    - 138
                    - 44
                    - 32
                # パーツをサブ色で設定するときは、`パーツ名-sub`というキーで設定する
                eyeshadow-sub: imake/static/modes/custom/eyeshadow/eyeshadow0-0.png
                eyeshadow-color: # (hue, saturation, value) = (360deg, 100%, 100%)
                    - 138
                    - 44
                    - 32
    questions:
        1:
            text: 手のひらの色
            choices:
                -   text: 黄みピンク～オレンジっぽい
                    answer_id: blue_base (answersにあるIDの中から選択)
                    next_node_id: 2
                -   text: 青みピンク~赤紫っぽい
                    answer_id: yellow_base
                    next_node_id: 2
        2:
            ...
"質問(Node)のID2":
    ...
```

- next_node_id が null(or 記述なし) の場合は、そのセクションの質問が終了を意味する
- 最初の質問のIDは `1` というキーで設定する
