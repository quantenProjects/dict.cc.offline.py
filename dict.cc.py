import readline
import sqlite3
import sys


# code from https://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python :D
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
        # try:
        #    cr = (env['LINES'], env['COLUMNS'])
        # except:
        #    cr = (25, 80)
    return int(cr[1])


# get terminalwidth for formating the output
terminalwidthhalf = int(getTerminalSize() / 2)

# choosing language from comand line argument
if len(sys.argv) >= 2:
    if sys.argv[1] == "d":
        lang = 1
    elif sys.argv[1] == "e":
        lang = 2
else:
    lang = 1


def lang_to_char():
    return "de"[lang - 1]


conn = sqlite3.connect('dict.cc.db')  # connect to db
c = conn.cursor()

# start info
print("python cmd line interface for dict cc sqlite db deutsch englisch")
print("enter e for englisch search, enter d for german search")
print("use tab (double tap) for autocompletion")
print("use CTRL + c for exiting")


# returning the bash color codes, first line black, then red, black, grey
def colors(n):
    if n % 4 == 1:
        return '\033[48;5;196m'  # red
    elif n % 4 == 3:
        return '\033[48;5;245m'  # grey
    else:
        return ''


def completer(text, state):  # completer for autocompletion
    suggestes = suggest(text)
    options = [x for x in suggestes if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None


def suggest(term):  # function for suggestes
    first_char = term.lower()[0]
    if 'a' <= first_char <= 'z':
        first_char = "_" + first_char
    else:
        first_char = ""
    term = (str(term + "%"), lang)  # create tupel for sqlite3
    c.execute(f"SELECT term4search FROM singlewords{first_char} WHERE term4search like ?  and colnum = ? limit 10", term)
    result = []
    for i in c.fetchall():
        result.append(i[0])
    return result


def searchindb(text):  # real searching
    searchterm = (str(text + "%"),)
    # print searchterm
    c.execute(f"SELECT * FROM main_ft WHERE term{lang} like ? order by vt_usage DESC , sort2 , sort1 limit 60 ",
                  searchterm)
    res = c.fetchall()
    j = 0
    for i in res:
        print(colors(j), i[1].ljust(terminalwidthhalf), i[2].ljust(terminalwidthhalf - 8),
              '\033[49m')  # formating output
        # print '' ##uncomment for result every second line
        j += 1



# setting up the autocompleter
readline.set_completer_delims("")
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

while True:
    inp = input(lang_to_char() + "> ")  # searchterm input

    # checking for language change
    if inp == "e":
        lang = 2
        continue
    elif inp == "d":
        lang = 1
        continue

    searchindb(inp)  # searching
