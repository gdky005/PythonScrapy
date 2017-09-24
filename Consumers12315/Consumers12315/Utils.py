import re


def sliptStr(context, startStr, endStr):
    start = context.find(startStr) + startStr.__len__()
    end = context.find(endStr)
    currentId = context[start:end]
    return currentId


def matchTitle(text):
    match = re.match(r'[1-9]\d*\.', text)
    if None != match:
        return True
    return False


def isEndChar(text):
    char = ["。", "？", "”", "！", "："]
    endChar = text[len(text) - 1]
    for c in char:
        if c == endChar:
            return True
    return False