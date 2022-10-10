# Custom Mode

## Directory Structure

メイク画像は各パーツ(部分)ごとにディレクトリを切って格納

```sh
.
├── README.md
├── color.png
├── menu.png
├── icon.png
├── eyebags
│   ├── eyebags0.png
│   ├── eyebags1.png
│   ├── eyebags2.png
│   ├── thumbnail.png # パーツのサムネイル画像
│   └── thumbnails # メイク画像と同じ名前でサムネイル画像を格納
│       ├── eyebags0.PNG
│       ├── eyebags1.PNG
│       └── eyebags2.PNG
├── eyebrow
│   ├── eyebrow arch.png
│   ├── eyebrow drop.png
│   ├── eyebrow straight.png
│   ├── eyebrow thick.png
│   ├── eyebrow upward.png
│   ├── thumbnail.png
│   └── thumbnails
│       ├── eyebrow arch.png
│       ├── eyebrow drop.png
│       ├── eyebrow strait.png
│       ├── eyebrow thick.png
│       └── eyebrow upward.png
...
└── u-glitter
    ├── thumbnail.png
    ├── u-glitter base.png
    ├── u-glitterL.png
    ├── u-glitterM base.png
    ├── u-glitterM.png
    ├── u-glitterS base.png
    └── u-glitterS.png
```

## Naming Rules

- ２枚重ねによって表現されるパーツは、色変更する画像を `hoge.png` として、色変更しない画像を `hoge-base.png` とする

## Order

order.ymlには、パーツを表示する際の順番を記述する。（表記のないものは、表記のあるものの以降に順不同で表示される。）

```yaml
order:
    - double
    - eyebrow
```
