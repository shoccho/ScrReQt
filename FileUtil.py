from pathlib import Path
from datetime import datetime


def getDocumentsFolder():
    return Path.home() / "Documents"


def getFilename():
    now = datetime.now()
    current_time = now.strftime("Screen_Record_%H_%M_%S")
    return current_time + ".mkv"


def getFileNameWithPath():
    return f'{getDocumentsFolder()}/{getFilename()}'


if __name__ == "__main__":
    print(getDocumentsFolder())
    print(getFilename())
