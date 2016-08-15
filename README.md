# resmonlog (Resource Monitor Logger)

This script will periodically poll the system for various resource statistics and log it to a file.

## Running

```
$ python resmonlog.py
```

## Help

```
$ python resmonlog.py -h
usage: resmonlog.py [-h] [-j JSON_FILE] [-c CSV_FILE] [-p PERIOD]

A simple python script template.

optional arguments:
  -h, --help            show this help message and exit
  -j JSON_FILE, --json-file JSON_FILE
                        JSON formatted log file
  -c CSV_FILE, --csv-file CSV_FILE
                        CSV formatted log file
  -p PERIOD, --period PERIOD
                        Period in seconds for logging data (Default: 30)
```
