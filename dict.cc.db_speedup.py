from shutil import copyfile
import sqlite3

conn = sqlite3.connect('dict.db')
c = conn.cursor()

print "This will change the db file 'dict.db' in the current folder. The file could be damaged, please make a backup"
print "enter YES for making backup (to 'dict_backup.db') and optimise db."
print "enter NO_BACKUP for optimise db without backup (when you have not so much diskspace"
print "enter anything else to abort"
inputstr = raw_input(">")
if inputstr == "YES":
    print "making backup. this may take some time"
    copyfile('dict.db', 'dict_backup.db')
    print "backup completed"
elif inputstr == "NO_BACKUP":
    print "skiping backup"
else:
    print "quiting"
    quit()
    
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='singlewords1'")
if len(c.fetchall()) == 1:
    print "db is already optimised, quiting"
    quit()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='singlewords'")
if len(c.fetchall()) == 1:
    print "slow db structure detected, begining"
else:
    print "cannot detect db state"
    quit()

print "creating new tables"
c.execute("CREATE TABLE singlewords1(term4search VARCHAR);")
c.execute("CREATE TABLE singlewords2(term4search VARCHAR);")
print "copy data"
print "first table"
c.execute("INSERT INTO singlewords1 SELECT term4search FROM singlewords WHERE colnum = 1")
print "second table"
c.execute("INSERT INTO singlewords2 SELECT term4search FROM singlewords WHERE colnum = 2")
print "create indexes"
print "first table"
c.execute("CREATE INDEX 'singlewords1_index' ON 'singlewords1' ('term4search' ASC)")
print "second table"
c.execute("CREATE INDEX 'singlewords2_index' ON 'singlewords2' ('term4search' ASC)")
print "drop old table"
c.execute("DROP TABLE singlewords")
print "clean up db"
c.execute("VACUUM;")
