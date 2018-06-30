# bro2csv
Take Bro .log files and output as csv. Logs must be \*.log (or the glob can be specified with --glob argument)

Original usecase was to convert bro logs for use with Vega Voyager 2 (https://github.com/vega/voyager/)

# Example uses:

Save bro log dir straight to csv
### ./bro-csv.py -i ~/vmshare/

Save csv to current dir
### ./bro-csv.py -i ~/vmshare/ --cwd

Overwrite existing files
### ./bro-csv.py -i ~/vmshare/ --overwrite

Define fields to output (if --fields is unspecified it will save all)
### ./bro-csv.py -i ~/vmshare/ -f id.orig_h id.resp_h host referrer 

Output to standard out and align on csv columns!
### ./bro2csv.py -i ~/vmshare/http.log --stdo | column -ts ',' | less -S

# Full help
```
$ python bro2csv.py --help
usage: bro2csv.py [-h] -i ./bro_logs/http.log [./bro_logs/http.log ...]
                  [-f host [host ...]] [--overwrite] [--stdo] [--cwd]
                  [--glob "*.log"]

Translate bro logs (TSV) to CSV

optional arguments:
  -h, --help            show this help message and exit
  -i ./bro_logs/http.log [./bro_logs/http.log ...], --input ./bro_logs/http.log [./bro_logs/http.log ...]
                        Specific bro log path - individual file or directory.
                        Must be .log
  -f host [host ...], --fields host [host ...]
                        Bro output fields
  --overwrite           Overwrite any existing files
  --stdo                Print to standard out (as csv)
  --cwd                 Save files to the current working directory instead of
                        beside original files.
  --glob "*.log"        Glob for bro logs. Must be quoted, e.g. "*.log" -
                        can't be used when the input is a file (obviously...)
```
