# Migration from Etherpad to CodiMD

## Step 1: extract the data from MySQL

The data is stored as a `(key, value)` pairs, with keys being for:
 - `globalAuthor:<identifier>`
 - `pad:<pad_name>`
 - `pad:<pad_name>:revs:<identifier>`
 - `comments:<pad_name>`
 - `readonly2pad:<identifier>`
 - `pad2readonly:<identifier>`
 - `sessionstorage:<identifier>`
 
Values for each type of keys is stored as a json string.
Here we are only interested by the content of each pads, their comments and the authors.


You can get a CSV dump by executing:
```bash
mysql --user=etherpad --password etherpad-lite < request.sql | sed 's/\t/,/g' > etherpad_dumb.csv
```

You have to adapt this if you are using different users settings for the database.

## Step 2: extracting the data

You can extract info from the csv using the Python 3 script
```ven
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt # actually just pandas
```

and then this:
```bash
chmod +x extract.py
./extract.py etherpad_dumb.csv out
```
