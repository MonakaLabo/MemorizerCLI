# logger.pyの使用方法

## 0. 概要

ロギング用のプログラム。

```python
# import
from programs.logger import get_logger

# logging
logger = get_logger()
logger.info("message")
```

## 1. 使用方法

ログには4種類あり、重要度に応じて使い分ける。

```python
logger.debug("開発用")
logger.info("通常ログ")
logger.warning("警告")
logger.error("エラー")
```

## 2. 出力

CLI上と `logs/autofilename.log` に記録される。