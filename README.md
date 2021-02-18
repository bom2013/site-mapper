# site-mapper
A simple python brute force site mapper.  
This project is based in part on code from the great book ["Black hat python"](https://www.amazon.com/Black-Hat-Python-Programming-Pentesters/dp/1593275900
 "Black hat python on Amazon")
## How it's work?
The software scans the website using a word-driven Brute Force search for pages that are open to access
## Install
1. Run: git clone https://github.com/bom2013/site-mapper or download this repo
2. Run the software :)
## How to use?
The software supports a variety of arguments, but the most basic usage is as follows:  
```sh
python ./site_mapper.py http://testphp.vulnweb.com
```
There are many optional arguments(most of them have default value).  
#### Number of threads
The software uses threads to speed up the scanning process, the amount of threads can be determined using the `-t` option
```sh
python ./site_mapper.py http://testphp.vulnweb.com -t 10
```
#### Words file
You can change the default words file(The default is "all.txt" file from [SVNDigger](https://www.netsparker.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/ "SVN Digger wordlist")) using the `-w` option
```sh
python ./site_mapper.py http://testphp.vulnweb.com -w wordFile.txt
```
#### Export result to file
By default, the software prints the scan results to the screen, if you want to send to a file instead, you can use the `-f` option
```sh
python ./site_mapper.py http://testphp.vulnweb.com -f result.txt
```
#### Mapping the status code to the full name
By default the software only displays the code status of each mapped page, if you want it to also display the full name of the code status you can use the `-s` option
```sh
python ./site_mapper.py http://testphp.vulnweb.com -s
```
#### Remove non-200 results
By default, the software displays all pages that do not return status 404, if you want the software to filter and display only pages that return status 200, you can use the `-r` option
```sh
python ./site_mapper.py http://testphp.vulnweb.com -r
```
#### Add file extensions to search
By default, the software goes through all the names in the word file and tries them. If you want the software to try not only the names but also try to add certain file extensions to them, you can use the `-e` option and then a list of extensions.  
For example, suppose the word file contains the word "admin" and you want the software to try not only "admin" but also "admin.php", "admin.html" etc. you can use the following code:
```sh
python ./site_mapper.py http://testphp.vulnweb.com -e .html .php
```
### Summary table
Option | Short name | Full name | Type | Default value
--- | --- | --- | --- | --
Number of threads | `-t` | `--thread` | `int` | 5
Word file address | `-w` | `--wordfile` | `str` | all.txt
Export to file | `-f` | `--file` | str | `str` | 
Show full name for statuc code | `-s` | `--status` | | 
Remove non-200 response | `-r` | `--remove` | | |
Add file extensions | `-e` | `--extension` | | |
## A note about copyright
The *[all.txt](https://github.com/bom2013/site-mapper/blob/main/all.txt "all.txt")* file is from [SVNDigger](https://www.netsparker.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/ "SVN Digger wordlist")) and it's licensed under GPL. 
## Contribution
Any contribution is welcome, just send a PR :)
