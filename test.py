def iAmSputid():
    data = []
    while(True):
        try:
            data.append(input())
        except EOFError:
            break
    print(list(reversed(data)))

iAmSputid()