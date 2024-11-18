#!/bin/bash

directory="/Users/muneer78/Downloads/"
file="non-fiction.md"

perl -ne '
    if (!/:/) {
        open(my $fh, ">>", "to-update.md");
        print $fh $_;
        close($fh);
    } else {
        open(my $fh, ">>", "non-fiction-updated.md");
        print $fh $_;
        close($fh);
    }
' "$directory/$file"
