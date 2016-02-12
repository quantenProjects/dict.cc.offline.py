import readline
import sqlite3
import os



#code from https://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python :D
def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1])



terminalwidthhalf = int(getTerminalSize()/2)
lang = "d"
conn = sqlite3.connect('dict.db')
c = conn.cursor()

print "python cmd line interface for dict cc sqlite db deutsch englisch"
print "enter e for englisch search, enter d for german search"
print "use tab (double tap) for autocompletion"
print "use CTRL + c for exiting"

def colors(n):
    if n%4==1:
        return '\033[48;5;52m'
    elif n%4==3:
        return '\033[48;5;236m'
    else:
        return ''

def completer(text, state):
    suggestes = suggest(text)
    options = [x for x in suggestes if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

def suggest(term):
    term = (str(term + "%"),)
    if lang == "e":
        c.execute('SELECT term4search FROM singlewords WHERE term4search like ?  and colnum = 2 limit 10',term)
    else:
        c.execute('SELECT term4search FROM singlewords WHERE term4search like ? and colnum = 1  limit 10',term)
    res = c.fetchall()
    j = 0
    result = []
    for i in res:
        result.append(i[0])
        #j += 1
    return result

def searchindb(text):
    searchterm = (str(text + "%"),)
    #print searchterm
    if lang == "e":
        c.execute('SELECT * FROM main_ft WHERE term2 like ? order by vt_usage DESC , sort2 , sort1 limit 60 ',searchterm)
    else:
        c.execute('SELECT * FROM main_ft WHERE term1 like ? order by vt_usage DESC , sort1 , sort2 limit 60 ',searchterm)
    res = c.fetchall()
    resdeu = ""
    reseng = ""
    j = 0
    for i in res:
        print colors(j), i[1].ljust(terminalwidthhalf),i[2].ljust(terminalwidthhalf-8),'\033[49m'
        #print '' ##uncomment for result every second line
        j+=1
       #resdeu += i[1] +"\n"
       

#c.execute('SELECT * FROM main_ft WHERE term1 like ? order by vt_usage DESC , sort1 , sort2',searchterm)

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")
while True:
    inp = raw_input(lang + "> ")
    if inp == "e":
        lang = "e"
        continue
    elif inp == "d":
        lang = "d"
        continue
    searchindb(inp)
