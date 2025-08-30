#!/usr/bin/perl

use strict;
use warnings;
use Text::CSV;
use IO::File;

# Sample data (you can replace this with data from a file if needed)
my @input_data = (
    "John, Doe, 30",
    "Jane, Smith, 25",
    "Alice, Johnson, 40"
);

# Output CSV file name
my $output_filename = "output.csv";

# Create a CSV writer
my $csv = Text::CSV->new({ binary => 1, eol => $/ }) or die "Cannot use Text::CSV: " . Text::CSV->error_diag();

# Open output file for writing
my $fh = IO::File->new(">$output_filename") or die "Cannot open $output_filename: $!";

# Write header
$csv->print($fh, ["col_1", "col_2", "col_3"]);

# Process each line in input_data
foreach my $line (@input_data) {
    # Split by comma and optional space
    my @fields = split /\s*,\s*/, $line;
    $csv->print($fh, \@fields);
}

$fh->close;
print "Data has been written to $output_filename\n";
