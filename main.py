import sys, getopt, os, shutil
import zlib
import r2pipe
from article import loadHashes
from hash40 import Hash40
from parseAnimcmdList import ParseAnimcmdList
from parseAnimcmdStart import ParseAnimcmdStart
from scriptparser import Parser
from methodInfo import methodInfo, loadMethodInfo

output = "output"
parserOutput = "parser"
scriptCategory = "game"
parseScripts = False

categories = ['game', 'effect', 'sound', 'expression']

def dump(file):
    global output, parserOutput, scriptCategory, parseScripts, methodInfo
    print("Opening file {0}".format(file))
    filename = os.path.split(os.path.splitext(file)[0])[-1]
    loadHashes(scriptCategory + "_")

    if 'common' in filename or 'item' in filename:
        return

    r2 = r2pipe.open(file)
    r2.cmd('e anal.bb.maxsize = 0x10000')
    r2.cmd('e anal.vars = false')
    sections = r2.cmdJ("isj")
    loadMethodInfo(sections)
    game = next((x for x in sections if "lua2cpp::create_agent_fighter_animcmd_{0}_".format(scriptCategory) in x.demname and "_share_" not in x.demname), None)
    if game:
        print("{0} found".format(game.demname))

        af = r2.cmdJ('s {0};af;pdfj'.format(game.vaddr))
        
        p = ParseAnimcmdList(r2, af, sections)

        print("Scripts extracted") #, {0} articles found .format(len(p.ArticleScripts))

        if not os.path.exists(output):
            os.makedirs(output)
        
        if not os.path.exists("{0}/{1}".format(output, filename)):
            os.makedirs("{0}/{1}".format(output, filename))

        if parseScripts:
            if not os.path.exists(parserOutput):
                os.makedirs(parserOutput)
        
            if not os.path.exists("{0}/{1}".format(parserOutput, filename)):
                os.makedirs("{0}/{1}".format(parserOutput, filename))

        if len(p.Issues) > 0:
            #Log missing scripts in file due to issues on parsing or radare2 output
            None
            #f = open("{0}/{1}/{2}.txt".format(output, filename, "missing"), "w")
            #f.write("")
            #f.close()

        for article in p.ArticleScripts:
            
            print("Dumping article {0} scripts, count: {1}".format(article.findHashValue(), len(article.scriptsHash)))

            if not os.path.exists("{0}/{1}/{2}".format(output, filename, article.findHashValue())):
                os.makedirs("{0}/{1}/{2}".format(output, filename, article.findHashValue()))

            if parseScripts:
                if not os.path.exists("{0}/{1}/{2}".format(parserOutput, filename, article.findHashValue())):
                    os.makedirs("{0}/{1}/{2}".format(parserOutput, filename, article.findHashValue()))
            
            for hash in article.scriptsHash:
                
                scriptStart = r2.cmdJ('s {0};pdj 20'.format(hash.address))
                scriptAddress = ParseAnimcmdStart(scriptStart).address

                if scriptAddress:
                    script = r2.cmdJ('s {0};aF;pdfj'.format(scriptAddress))

                    if parseScripts:
                        try:
                            parser = Parser(r2, script, hash.findHashValue(), sections)
                            pf = open('{0}/{1}/{2}/{3}.txt'.format(parserOutput, filename, article.findHashValue(), hash.findHashValue()),'w')
                            pf.write(parser.Output())
                            pf.close()
                        except:
                            print("Couldn't parse {0}".format(hash.findHashValue()))

                    #script = script.replace('\r', '')
                    #exists = os.path.exists("{0}/{1}/{2}/{3}.txt".format(output, filename, article.findHashValue(), hash.findHashValue()))
                    #if not exists:
                    #f = open("{0}/{1}/{2}/{3}.txt".format(output, filename, article.findHashValue(), hash.findHashValue()), "w")
                    #f.write(script)
                    #f.close()
                    #else:
                    #    v = 2
                    #    while exists:
                    #        exists = os.path.exists("{0}/{1}/{2}/{3} ({4}).txt".format(output, filename, article.findHashValue(), hash.findHashValue(), v))
                    #        if not exists:
                    #            f = open("{0}/{1}/{2}/{3} ({4}).txt".format(output, filename, article.findHashValue(), hash.findHashValue(), v), "w")
                    #            f.write(script)
                    #            f.close()
                    #        v += 1

    else:
        print('animcmd_game not found on file {0}'.format(file))
    
    r2.quit()

def Parse(file):
    script = open(file, 'r')
    t = script.read()
    t = t.replace('\n','\n\r')
    p = Parser(None, t)

def start(path, argv):
    global output, parseScripts, categories, scriptCategory
    try:
      opts, args = getopt.getopt(argv,"o:pc:",["output=", "category="])
    except getopt.GetoptError:
        print('main.py path')
        print("file path: dump scripts from elf file")
        print("directory path: dump all scripts from elf files found on directory")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-o':
            output = arg
        if opt == '-p':
            parseScripts = True
        if opt == '-c':
            if arg in categories:
                scriptCategory = arg
            else:
                print("{0} is not a valid script category".format(arg))
                print("categories: {0}".format(categories))
                sys.exit(2)

    run = False

    if os.path.isdir(path):
        for file in os.listdir(path):
            if os.path.splitext(file)[1] == ".elf": 
                run = True
                dump(os.path.join(path,file))
    elif os.path.isfile(path):
        ext = os.path.splitext(path)
        if os.path.splitext(path)[1] == ".elf":
            run = True
            dump(path)

    if not run:
        print("No elf file found")

    print("Done!")


if __name__ == "__main__":
    start(sys.argv[1], sys.argv[2:])