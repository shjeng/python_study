trueCharList = ["T", "R", "U", "E"]
loveCharList = ["L", "O", "V", "E"]
trueCount = 0
loveCount = 0


def calculate_love_score(name1, name2):
    name1 = name1.upper()
    name2 = name2.upper()
    for index in range(0, 4):
        tChar = trueCharList[index]
        lChar = loveCharList[index]

        if tChar in name1:
            trueCount = trueCount + name1.count(tChar)
        if tChar in name2:
            trueCount += name2.count(tChar)

        if lChar in name1:
            loveCount += name1.count(lChar)
        if lChar in name2:
            loveCount += name2.count(lChar)

