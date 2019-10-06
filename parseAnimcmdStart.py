from article import Article, ScriptHash
from hash40 import Hash40

class ParseAnimcmdStart:
    def __init__(self, ops):
        self.lines = []
        for op in ops:
            self.lines.append(op.disasm)
        
        #Process
        self.address = None
        for line in self.lines:
            #print(line)
            t = line.split(' ')
            instr = t[0]
            val = ''.join(t[1:])
            if instr == 'bl':
                if "0x" in val or "fcn." in val:
                    self.address = int(val.replace("fcn.", "0x"), 16)
                    break
