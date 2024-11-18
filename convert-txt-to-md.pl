#!/usr/bin/perl

use strict;
use warnings;

# Open the input and output files
open(my $IN, '<', 'Hayes- Midnight Express.txt') or die "Could not open input file: $!";
open(my $OUT, '>', 'output.md') or die "Could not open output file: $!";

while (<$IN>) {
    chomp;

    # Recognize and convert headings
    if (/^#+\s+/) {
        print $OUT "#$_\n";
        next;
    }

    # Recognize and convert lists
    if (/^\s*-\s/) {
        print $OUT "  - $_\n";
        next;
    }

    # Recognize and convert bold and italic text
    s/\*\*(.*?)\*\*/\*\*$1\*\*/g; # Bold
    s/\*(.*?)\*/\*$1\*/g; # Italic

    # Print the line to the output file
    print $OUT "$_\n";
}

close($IN);
close($OUT);