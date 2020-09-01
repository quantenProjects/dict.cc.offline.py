import readline
import sqlite3
import os
import sys

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


#get terminalwidth for formating the output
terminalwidthhalf = int(getTerminalSize()/2) 

#choosing language from comand line argument
if len(sys.argv) >= 2:
    if sys.argv[1] == "d":
        lang = "d"
    elif sys.argv[1] == "e":
        lang = "e"
else:
    lang = "d"
   

conn = sqlite3.connect('dict.cc.db') #connect to db
c = conn.cursor()

#start info
print ("python cmd line interface for dict cc sqlite db deutsch englisch")
print ("enter e for englisch search, enter d for german search")
print ("use tab (double tap) for autocompletion")
print ("use CTRL + c for exiting")

#checking if db is fastdb structure
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='singlewords1'")
if len(c.fetchall()) == 1:
    fastdb = True
    print ("Fast db structure detected")

#returning the bash color codes, first line black, then red, black, grey
def colors(n):
    if n%4==1:
        return '\033[48;5;196m' #red
    elif n%4==3:
        return '\033[48;5;245m' #grey
    else:
        return ''

def completer(text, state): #completer for autocompletion
    suggestes = suggest(text)
    options = [x for x in suggestes if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

def suggest(term): #function for suggestes
    term = (str(term + "%"),) #create tupel for sqlite3
    if lang == "e":
        if fastdb:
            c.execute('SELECT term4search FROM singlewords2 WHERE term4search like ? limit 10',term)
        else:
            c.execute('SELECT term4search FROM singlewords WHERE term4search like ?  and colnum = 2 limit 10',term)
    else:
        if fastdb:
            c.execute('SELECT term4search FROM singlewords1 WHERE term4search like ? limit 10',term)
        else:
            c.execute('SELECT term4search FROM singlewords WHERE term4search like ? and colnum = 1  limit 10',term)
    res = c.fetchall()
    j = 0
    result = []
    for i in res:
        result.append(i[0])
        #j += 1
    return result

def searchindb(text): #real searching
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
        print (colors(j), i[1].ljust(terminalwidthhalf),i[2].ljust(terminalwidthhalf-8),'\033[49m') #formating output
        #print '' ##uncomment for result every second line
        j+=1
       #resdeu += i[1] +"\n"
       

#c.execute('SELECT * FROM main_ft WHERE term1 like ? order by vt_usage DESC , sort1 , sort2',searchterm)

#setting up the autocompleter
readline.set_completer(completer) 
readline.parse_and_bind("tab: complete")

while True:
    inp = input(lang + "> ") #searchterm input
    
    #checking for language change
    if inp == "e":
        lang = "e"
        continue
    elif inp == "d":
        lang = "d"
        continue
    
    searchindb(inp) #searching
