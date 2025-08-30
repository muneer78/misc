# Linux

## awk

```

# compare files to remove dupes from one in another
awk 'NR == FNR{ a[$0] = 1;next } !a[$0]'  >> RtsTransactionsFtp2025-03-17_fixed.csv RtsTransactionsFtp2025-03-17.csv RtsTransactionsFtp2025-03-17_new.csv

## write only 1st and 2nd column of file, using white space as delimiter
awk '{print $1, $2}' log.txt

# set delimiter when choosing columns
awk -F "," '{print $1, $2}' log.txt

# find lines common in all files
awk '(NR==FNR){a[$0]=1;next}
     (FNR==1){ for(i in a) if(a[i]) {a[i]=0} else {delete a[i]} }
     ($0 in a) { a[$0]=1 }
     END{for (i in a) if (a[i]) print i}' file1 file2 file3 ... file200
     
# filtering rows based on a condition
awk '$4 > 169' data.txt

# printing lines containing specific word
awk '/John/' data.txt

# Find dupe files
# Create the SQLite database and table
sqlite3 files.db "CREATE TABLE files (path TEXT, md5 TEXT, mod_date TEXT);"

# Import the CSV data into the SQLite table
sqlite3 files.db <<EOF
.mode csv
.import output.csv files
EOF

# Query the database for duplicates and sort the results
sqlite3 files.db <<EOF
.mode csv
.output duplicates_sorted.csv
SELECT path, md5, mod_date
FROM files
WHERE md5 IN (
    SELECT md5
    FROM files
    GROUP BY md5
    HAVING COUNT(md5) > 1
)
ORDER BY md5, mod_date;
EOF

# look at csv results
cat duplicates_sorted.csv

# Remove duplicate lines and save the rest into a new file
awk ‘!seen[$0]++’ filename > newfile

# vlookup
join -t, <(sort -nst, -k1,1 File2.csv) <(sort -nst, -k1,1 File1.csv)

```


## bash

```

# read pdfs
acroread /a "page=NUM & zoom=NUM

# compare 2 files
comm file1.txt file2.txt

# find files by prefix
compgen -f fzf

# compares the sorted versions of two files without creating intermediate files
diff <(sort file1.txt) <(sort file2.txt)

# finding files by name
find /path/to/search -name treasure

# finding files by name, case insensitive
find /path/to/search -iname treasure

# find by size
find /path/to/search -type f -size +1G -size -100G

# find file by days since last modified
find /path/to/search -mtime -7

# find files modified in specific month
find /path/to/search -type f -newermt "2024-10-01" ! -newermt "2024-11-01"

# enable globstar and list all text files in dirs and subdirs
shopt -s globstar
ls **/*.txt

# enable extglob and delete all files except those ending with .txt

shopt -s extglob
rm !(*.txt)

# combine pdfs
pdftk file1.pdf file2.pdf cat output combined.pdf

# remove duplicate lines in file.txt
sort file.txt | uniq 

```

### aliases

```

# Never accidentally delete a file again
alias rm='rm -i'

# Safely move and copy data
alias mv='mv -iv'
alias cp='cp -iv'

# Colorize grep
alias grep='grep --color'

# weather forecast
alias weather3="curl -s 'wttr.in/london?F'"
alias weather=”curl -s ‘wttr.in/meyrin+switzerland?1F’”
alias fancy_weather=”curl ‘wttr.in/nashville?format=v2’”


```

### functions

```

function pdf_to_png () {
    local pdf="${1}"
    local png=${pdf%.*}".png"

    convert -density 800 "${pdf}" -quality 100 "${png}"
}




```

## jq

```

# parse 
for file in *.json; do
    jq 'select(.SalesforceResponse != null) | del(.salesforce_response_metrics, .input_file) | .SalesforceResponse as $sf | del(.SalesforceResponse) | . + $sf' "$file" > "filtered_$file"
done

# convert to csv
jq -r '(.[0] | keys_unsorted) as $keys | $keys, map([.[ $keys[] ]])[] | @csv' filtered_*.json > combined_output.csv

```

## sed

```

#remove double quotes from title tag
sed -i.bak 's/^title: "\([^"]*\)"/title: \1/' *.md
sed -i.bak 's/^date: "\([^"]*\)"/title: \1/' *.md
rm *.bak

#Add new line to front matter
sed -i.bak '/^tags:/a\
layout: post
' *.md

# To remove bak files
rm *.bak

# substituting string with replacement in file.txt
sed 's/old/new/' file.txt

# convert all lowercase letters to uppercase in textfile.txt
sed 's/.*/\U&/' textfile.txt

# Text substitution (reading from file and saving to the same file)
sed -i -e 's/find/replace/g' teste

# Add a newline only if it doesn’t exist
echo "" >> file;  sed -ie '/^$/d;$G' file; sed -ie '/^$/d;$G' file


```

## zsh

### Globbing

#### regular
```
# Match all .txt files in the current directory
*.txt

# Match files like file1.txt, file2.txt, etc., in the current directory
file?.txt

# Match all .txt files recursively within directories
**/*.txt

# move all jpg and png files to specific dir
cp *.{jpg,png} images/

# Change the extension of filename from .txt to .md
${filename%.txt}.md

# Convert a filename variable to lowercase
${file:l}
```

#### extended globbing

```

Enable extended globbing with the following command:

setopt EXTENDED_GLOB

ls *(.) - List only regular files.
ls *(/) - List only directories.
ls *(-/) - List only directories and symbolic links to directories.

```

#### find

```

# find all gif files in a dir or subdir 
find . -type f -name '*.gif' -exec sh -c \
'file "$0" | grep -q "animated"' {} \; -print

# print all files to be deleted to terminal
find ~/ -name ".EagleFiler Metadata.plist" -print

# move all files to Trash
find ~/ -name ".EagleFiler Metadata.plist" -exec mv {} ~/.Trash/ \;

```

#### misc

```

---
# add to mac path
# 1. Navigate to the bin folder for your CLI application in your command line
# run pwd to “print working directory.
pwd

# append the directory to the $PATH using the following command
path+=('/Users/yourcomputer/Documents/google-cloud-sdk/bin')

# save PATH
export path
---

# append text to a file only if text does not exist
echo 'input text' | grep -xFv -f existing_file.txt >> existing_file.txt

```

#### wordcount

```

# count number of lines in file
wc -l filename

# count characters in string
SO="stackoverflow"
echo -n "$SO" | wc -c

```

# MacOS
## caffeinate

```

# Adding the -d flag also prevents the display from going to sleep.
# Specifying an existing process with -w <pid> automatically exits the caffeinate command once the specified process exits.
# Passing a command with caffeinate <command> starts the given command in a new process and prevents sleep until that process exits.

caffeinate -u -t -d -w 1234556 <seconds>

---

screencapture -c takes a screenshot and copies it to the clipboard.

screencapture <file> takes a screenshot and saves it to the given file.

Add the -T <seconds> flag to take the screenshot after the given delay in seconds.

---

# The possible values for -convert are: txt, html, rtf, rtfd, doc, docx
textutil -convert html journal.doc # converts journal.doc into journal.html

```

# Windows

## cmd

```

# compare two files and print lines with diffs
FC file1.ext file2.ext

# compare multiple files
comp log1.txt log2.txt log3.txt

# find all lines with search term in a file
find "type" header-compare.csv

# sort file
sort sample.txt

# view contents page by page
more long_text.txt

# clear screen
cls

# display or set date
date

# rename files
ren header-compare-PC-010536.csv header-compare-saved.csv

# display or set time
time

# move files from one dir to another
move 

# display tree structure of dir
tree

# display all active system tasks
tasklist

# kill active system task by calling the task id
taskkill /pid 1234

# test system connectivity
ping

```

## powershell

### misc
```

# split strings
("Hello world").split("ll"" ")

# extract substrings
("Hello world").Substring(2,5)

# replace string with another string
("Hello World").Replace("Hello","New")

# compare string
("Hello world").CompareTo("Hello" + " " + "world")

# format date
Get-Date -Format "dd-MM-yyyy"

# all add to date functions
$today = Get-Date
$today.AddYears(2).AddMonths(3).AddDays(1).AddHours(2).AddMinutes(10)

# get time between dates
$today = Get-Date
$Christmas = Get-Date -day 25 -month 12
New-TimeSpan -Start $today -End $christmas

# show calendar
get-calendar

# display tree structure of dir
tree

# compare files
compare-object (get-content one.txt) (get-content two.txt)

# find files modified in last 7 days
Get-ChildItem -Path "C:\Users\user\first - second" -Recurse |
    Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }
    
# get string length
$string = "Hello, World!"
$length = $string.Length
```

### json

```
---
# Define the directory containing the JSON files
$jsonDirectory = "C:\Users\mahmad\OneDrive - Ryan RTS\Downloads"
# Define the path for the output file
$outputFile = "C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\combined.json"

# Initialize an empty array to hold all JSON data
$allJsonData = @()

# Loop through each JSON file in the specified directory
Get-ChildItem -Path $jsonDirectory -Filter *.json | ForEach-Object {
    # Read and convert JSON content from each file
    $jsonData = Get-Content -Path $_.FullName | ConvertFrom-Json
    # Add the JSON data to the array
    $allJsonData += $jsonData
}

# Convert the combined array back to JSON format
$combinedJson = $allJsonData | ConvertTo-Json -Depth 10

# Write the combined JSON content to the output file
Set-Content -Path $outputFile -Value $combinedJson

# Read the combined JSON content from the output file
$jsonData = Get-Content -Path $outputFile | ConvertFrom-Json

# Loop through each record and output the 'SalesforceResponse' property
foreach ($record in $jsonData) {
    if ($record.PSObject.Properties["SalesforceResponse"]) {
        Write-Output $record.SalesforceResponse
    } else {
        Write-Output "SalesforceResponse property not found in record."
    }
}
---

# import json
$jsonData = Get-Content -Path “C:\path\to\your\data.json” -Raw | ConvertFrom-Json

# iterate through array
foreach ($service in $services) {
Write-Host “Service: $service”}

# export json
$jsonString | Set-Content -Path “C:\path\to\your\newdata.json”

# filter json
$filteredServices = $jsonData.Services | Where-Object { $_ -like “*Server*” }

```
