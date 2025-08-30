#!/bin/bash

directory="/Users/muneer78/Downloads/"
file="books.md"

perl -ne "
    if (/(.*?)\|/) {
        \$line = \$_;
        @fields = split(/\|/, \$line);
        \$has_fiction = 0;
        for (my \$i = 0; \$i < \$#fields; \$i++) {
            if (\$fields[\$i] =~ /fiction/i) {
                \$has_fiction = 1;
                last;
            }
        }
        if (\$has_fiction) {
            open(my \$fh, '>>', '$directory/fiction.md');
            print \$fh \$line;
            close(\$fh);
        } else {
            open(my \$fh, '>>', '$directory/non-fiction.md');
            print \$fh \$line;
            close(\$fh);
        }
    }
" "$directory/$file"
