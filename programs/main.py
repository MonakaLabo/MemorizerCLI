from logger import get_logger

logger = get_logger()

def tomain():
    # 外部からmain.pyを呼び出すときはここから実行
    logger.info("main.pyが実行されました")
    main()

def main():
    pass