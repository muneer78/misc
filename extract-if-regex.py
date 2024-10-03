import re

pattern = r'<DT><A HREF="(.*?)"'

with open('pb.txt', 'r') as input_file:
    for line in input_file:
        match = re.search(pattern, line)

        if match and 'TAGS="magary"' in line:
            url = match.group(1)

            with open('magary.txt', 'a') as output_file:
                output_file.write(url + '\n')