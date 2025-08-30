#!/usr/bin/perl

use strict;
use warnings;
use Text::CSV;
use IO::File;

# Function to print results
sub print_results {
    my ($output_file, $title) = @_;

    my $fh = IO::File->new($output_file, 'r') or die "Cannot open file '$output_file': $!";
    my $csv = Text::CSV->new({ binary => 1, auto_diag => 1 });

    my @rows;
    while (my $row = $csv->getline($fh)) {
        push @rows, $row;
    }
    $fh->close;

    my $total_rows = scalar @rows;
    print "Total rows: $total_rows\n";
    print "$title:\n";

    return if $total_rows < 1;

    my @headers = @{ $rows[0] };
    my $num_columns = scalar @headers;

    # For each column, collect and count values
    for my $col_idx (0 .. $num_columns - 1) {
        my %value_counts;
        foreach my $i (1 .. $#rows) {
            my $value = $rows[$i][$col_idx] // '';
            $value_counts{$value}++;
        }

        print "$headers[$col_idx]:\n";
        foreach my $val (sort keys %value_counts) {
            print "  $val: $value_counts{$val}\n";
        }
    }
    print "\n";
}

# Example usage
my $output_file = "combined_file.csv";
my $title = "Column Counts";

print_results($output_file, $title);
