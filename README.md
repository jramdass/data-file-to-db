# Data File to DB

## Overview

I created this program to pull data from files, mainly spreadsheets, and insert the data into a database.
Currently, it only works with .csv files and uses a SQLite DB as the output.

I want to do various personal projects with data sets such as building APIs, machine learning,
and creating data visualizations.

My favorite source for data is [Kaggle](https://www.kaggle.com/)

## How to use
1. Set values in `config` file
   1. `db_name` - name of output DB file
   2. `table_name` - name of table in DB
   3. `dataset_filename` - name of file to read data from
   4. `dataset_path` - path on disk to file from `3`
   5. `data_types` - a comma-separate list of data types for each column in the dataset file
        <br>**ex**. string, int, string, string, string, int, int, string, string, string, float, float
   6. `primary_key` - the name of the column to use as a primary key (enter the sanitized column name - leave blank if no primary key is needed)
   7. Run `data_file_to_db.py`
   8. Follow the program menu

## Future Improvements
- Expand to more input file types, not just .csv
- Expand to more output file types, not just sqlite
- More general header sanitization. Currently, it was made for the particular data .csv I was working with