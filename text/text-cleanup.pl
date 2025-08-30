#!/usr/bin/perl
use strict;
use warnings;

while (<>) {
    chomp;

    # Delete lines containing only a number
    next unless /^\D/;

    # Prepend "## " to lines starting with "CHAPTER"
    s/^CHAPTER/## CHAPTER/;

    print "$_\n";
}