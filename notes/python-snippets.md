# General Python code snippets

## Numpy
```
# Return pairwise Pearson product-moment correlation coefficients between columns. Requires numpy to be installed.
df.corr()
```

## Lambda functions
```

# filter
bricks = ["red", "blue", "red", "blue", "red", "blue"]
red_bricks = filter(lambda x: x == 'red', bricks)
print(len(list(bricks)))  # Output: 3

# map
bricks = ["red", "blue", "red", "blue", "red", "blue"]
green_bricks = map(lambda x: "green", bricks)
print(len(list(green_bricks)))  # Output: 6
```

# Regular expressions

```
# Replace text
replaced_text = re.sub(r"string", "sentence", text)
print(replaced_text)
```

## Misc scripts

```

# generate calendar in the terminal
python -m calendar 2024 11

# set date to today
from datetime import datetime as dt
date_today = dt.now()

# capitalize text
capitalized_text = text.capitalize()

# find most common element in a list
from collections import Counter

lst = [1, 2, 2, 3, 3, 3, 4]
most_common = Counter(lst).most_common(1)[0][0]

# get unique elements in list
lst = [1, 2, 2, 3, 3, 4]
unique_lst = list(set(lst))

# shuffle list
import random
lst = [1, 2, 3, 4]
random.shuffle(lst)

# generate a GUID
import uuid
guid = uuid.uuid4()

# check for leap year
def is_leap_year(year): return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Convert F to C
celsius = (fahrenheit - 32) * 5/9

# Create progress bar
import time from tqdm
import tqdm
for i in tqdm(range(100)): time.sleep(0.1)

# Get current working directory
import os

cwd = os.getcwd()

# Chain custom functions
result = (
    df.pipe(subtract_federal_tax)
      .pipe(subtract_state_tax, rate=0.12)
      .pipe(
          (subtract_national_insurance, 'df'),
          rate=0.05,
          rate_increase=0.02
      )
)
print(result)

# # Normalize numeric columns
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df[['numeric_column']] = scaler.fit_transform(df[['numeric_column']]

# pretty printing
import pprint
data = {'a': [1, 2, 3], 'b': [4, 5, 6]}
pprint.pprint(data)

# Assign: create a new DataFrame with additional columns, assigning values based on existing columns or operations
df.assign(value_cat=np.where(df["Value"] > 20, "high", "low"))
df.assign(value_cat=np.where(df["Value"] > 20, "high", "low")).groupby(
    "value_cat"
).mean()

# combine_first: choosing values from the first Series and filling in any missing values with the corresponding values from the second Series
s1 = pd.Series([1, 2, np.nan, 4, np.nan, 6])
s2 = pd.Series([10, np.nan, 30, 40, np.nan, 60])

s1.combine_first(s2)

s3 = pd.Series([1, 2, 3, 4, 5, 6])
s1.combine_first(s2).combine_first(s3)

# Sort List based on another List
list1 =  ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
list2 = [ 0, 1, 1, 1, 2, 2, 0, 1, 1, 3, 4]
C = [x for _, x in sorted(zip(list2, list1), key=lambda pair: pair[0])]
print(C) # ['a', 'g', 'b', 'c', 'd', 'h', 'i', 'e', 'f', 'j', 'k']

# Reading lines from a file until an empty line is encountered using walrus
# allows for assignment and return of a value within an expression
with open('myfile.txt') as file:
    while (line := file.readline().rstrip()):
        print(line)


# Data validation with enums
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

def assign_role(role: UserRole):
    if not isinstance(role, UserRole):
        raise ValueError(f"Invalid role: {role}")
    print(f"Role assigned: {role.name}")

# calculate exponent
print(pow(2, 2))

# add numbers
numbers = [1, 2, 3, 4, 5]

total = sum(numbers)

print(total)

```

# Logging

```
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create a file handler and set the logging level
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler and set the logging level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example usage
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')

# Here’s an example of how to configure logging using a configuration file (logging.conf):

[loggers]
keys=root

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler,fileHandler

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('app.log',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
To use this configuration file in your Python code, you can do the following:

import logging
import logging.config

# Load the logging configuration from the file
logging.config.fileConfig('logging.conf')

# Get the logger
logger = logging.getLogger(__name__)

# Example usage
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
```

# File manipulation

```
# getting all of a specific file type from a directory
import glob

# append multiple csvs
import csv

combined_data = []

for file in file_paths:
    with open(file, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            combined_data.append(row)


file_paths = glob.glob('path/to/csv/files/*.csv')

# Create a Path object
from pathlib import Path

path = Path('/path/to/directory')

# Access parts of the path
print(path.name)       # 'directory'
print(path.parent)     # '/path/to'
print(path.suffix)     # ''

# Join paths
path = Path('/path/to')
new_path = path / 'directory' / 'file.txt'

# Checking if path exits 
if path.exists():
    print("The file exists")
else:
    print("The file does not exist")

# Reading from a file
path = Path('/path/to/file.txt')
content = path.read_text()
print(content)

# Listing Directory Contents
for file in path.iterdir():
    print(file)

# resizing all images in a directory
from PIL import Image
import os

input_folder = 'path/to/images'
output_folder = 'path/to/resized_images'
new_size = (800, 800)

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Resize all images in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        img_resized = img.resize(new_size)
        img_resized.save(os.path.join(output_folder, filename))

print("All images resized successfully!")


# find files by extension

import os

directory = 'path/to/directory'
extension = '.csv'
files = [f for f in os.listdir(directory) if f.endswith(extension)]

print(files)

# file duplication finder

import os
import hashlib

def hash_file(filename):
    h = hashlib.md5()
    with open(filename, 'rb') as file:
        while chunk := file.read(8192):
            h.update(chunk)
    return h.hexdigest()

def find_duplicates(folder):
    hashes = {}
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            file_hash = hash_file(full_path)
            if file_hash in hashes:
                print(f"Duplicate found: {full_path} == {hashes[file_hash]}")
            else:
                hashes[file_hash] = full_path

find_duplicates('/path/to/your/folder')
```

# Generators

```
# Computes values only when needed, saving memory and processing time, especially with large datasets
def process_logs(filename):
    with open(filename) as file:
        for line in file:
            if "ERROR" in line:
                yield line

# Using a generator to process logs lazily
for log in process_logs("server.log"):
    print(log)
```