#!/usr/bin/perl

use strict;
use warnings;
use File::Basename;
use File::Spec;

# Define the pattern to match filenames starting with 'business'
my $pattern = qr/^business/;

# Set directory
my $directory = '/mnt/c/Users/mahmad/OneDrive - Ryan RTS/Downloads/checks'; # Change to your desired path

# Check if directory exists
unless (-d $directory) {
    print "Directory does not exist: $directory\n";
    exit 1;
}

# Open directory
opendir(my $dh, $directory) or die "Cannot open directory $directory: $!";

# Read and process files
while (my $file = readdir($dh)) {
    next if $file =~ /\.csv$/;         # Skip files ending in .csv
    next unless $file =~ $pattern;     # Skip files not starting with 'business'

    my $old_path = File::Spec->catfile($directory, $file);
    next unless -f $old_path;          # Only process regular files

    my $new_filename = "$file.csv";
    my $new_path = File::Spec->catfile($directory, $new_filename);

    rename $old_path, $new_path or warn "Failed to rename $file: $!";
    print "Renamed: $file to $new_filename\n";
}

closedir($dh);
