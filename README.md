# Extraction of Etherpad data

## Step 1: dump the data from MySQL

In the database the data is stored as a `(key, value)` pairs, with keys being for:
 - `globalAuthor:<identifier>`
 - `pad:<pad_name>`
 - `pad:<pad_name>:revs:<identifier>`
 - `comments:<pad_name>`
 - `readonly2pad:<identifier>`
 - `pad2readonly:<identifier>`
 - `sessionstorage:<identifier>`

Values for each type of keys are stored as json strings.
Here we are only interested by the content of each pad, 
their comments and the authors.


You can get a CSV dump by executing:
```bash
mysql --user=etherpad --password etherpad-lite < request.sql | sed 's/\t/,/g' > etherpad_dumb.csv
```

You may have to adapt this if you are using different users settings for your database.

## Step 2: extract the data to csv and json

You can extract info from the csv using the Python 3 script
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt # actually just pandas
```

and then this:
```bash
chmod +x extract.py
./extract.py etherpad_dumb.csv out
```

`out` will have the following structure:

```
$ tree out
out
├── authors.csv
├── comments
│   ├── pad01.json
│   ├── pad01.json
│   └── …
└── pads
    ├── pad01.txt
    ├── pad02.txt
    └── …
    
```

## License 

This project is distributed under the [BSD 3-Clause](./LICENSE).
