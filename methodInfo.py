methodInfo = {}

def loadMethodInfo(json):
    global methodInfo
    for s in json:
        if s.bind == "GLOBAL" and s.vaddr > 0:
            methodInfo[s.vaddr] = s.demname