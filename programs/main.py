from programs.logger import (
    get_logger,
    displaytoggle
)

logger = get_logger()

def tomain():
    # 外部からmain.pyを呼び出すときはここから実行
    logger.info("main.pyが実行されました")
    displaytoggle(False)
    main()

def main():
    logger.info("このログはCLIには表示されないはず")
    pass