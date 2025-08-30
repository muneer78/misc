#!/usr/bin/perl
use strict;
use warnings;

while (<>) {
    chomp;
    # Remove non-printable characters
    s/[[:cntrl:]]//g;
    # Remove other unknown characters (adjust as needed)
    s/[^\x20-\x7E]//g;
    print "$_\n";
}