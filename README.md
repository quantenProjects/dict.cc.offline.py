# dict.cc.offilne.py

cmd line dict for the android SQLite db from dict.cc written in python3

## Usage

simply start in the same folder, where the dict.cc.db is located.

```shell script
python3 dict.cc.py
```

Use "d" or "e" as command line arguments to preselect a language

d> means german (deutsch) search
e> means english search

Simply enter e or d to change the search direction

Use tab (also double tap) to get auto completion like in the shell. But be patient, the takes a second to generate the suggestions.

Use CTRL + C to exit the script.

Use % (percentage sign) as wildcard. For example to search for english verbs: % walk -> to walk. The script adds automatically a % to the end of your searchterm.

While % represents zero to infinity characters, _ (underscore) represents only one character. You can also use any other SQL wildcard.

Tipp for the Wildcard:

Use % eat (note the space between % and walk) to get "to eat" and not %eat which also results in "meat", "repeat" and "to beat".

## How to get the DB

This script uses the SQLite DB from the [dict.cc Android App](https://play.google.com/store/apps/details?id=cc.dict.dictcc)

The simplest way to get this DB, is to download the app, then download the dictionary in the app.
The DB will be downloaded to the cc.dict.dictcc folder on your phone.
Only copy the file to the same folder, where the script is located and rename the DB to "dict.db"

There is also a way to directly download the db, but this could be not allowed by dict.cc

## DB with other languages (Musrar)

It works perfectly fine if you change the .db to the one you want. Just be aware that the e> command is for the non-german language of your choice.
