from collections import namedtuple

methodInfo = {}

def loadMethodInfo(json):
    global methodInfo
    Method = namedtuple("Method", "name demname args")
    for s in json:
        if s.bind == "GLOBAL" and s.vaddr > 0:
            spl = s.demname.split('(')
            if len(spl) == 1:
                continue
            name = spl[0]
            args = []
            for x in spl[1].split(')')[0].split(","):
                args.append(x.strip())
            methodInfo[s.vaddr] = Method(name, s.demname, args)