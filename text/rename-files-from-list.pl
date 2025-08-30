#!/usr/bin/perl

use strict;
use warnings;
use File::Basename;
use File::Spec;

# Directory path containing the files
my $directory_path = "/Users/muneer78/Desktop/saved";

# Path to the CSV file (assumed to be in the same directory)
my $csv_file = File::Spec->catfile($directory_path, "updated_file.csv");

# Read the CSV into a hash: title => postdate
open my $csv_fh, '<', $csv_file or die "Could not open '$csv_file': $!";
my %title_to_postdate;

while (my $line = <$csv_fh>) {
    chomp $line;
    my ($title, $postdate) = split /,/, $line;

    next if $title eq 'title';  # Skip header

    $title_to_postdate{$title} = $postdate;
}
close $csv_fh;

# Iterate over each file in the directory
opendir(my $dh, $directory_path) or die "Cannot open directory $directory_path: $!";
while (my $file = readdir($dh)) {
    next if $file eq '.' or $file eq '..';
    next if -d File::Spec->catfile($directory_path, $file);
    next if $file eq "updated_file.csv";

    foreach my $title (keys %title_to_postdate) {
        if (index($file, $title) != -1) {
            if ($file =~ /(\d{4}-\d{2}-\d{2})/) {
                my $old_date = $1;
                my $new_date = $title_to_postdate{$title};

                (my $new_filename = $file) =~ s/\Q$old_date\E/$new_date/;

                my $old_path = File::Spec->catfile($directory_path, $file);
                my $new_path = File::Spec->catfile($directory_path, $new_filename);

                rename $old_path, $new_path or warn "Could not rename '$file' to '$new_filename': $!";
                print "Renamed: $file to $new_filename\n";
            }
        }
    }
}
closedir($dh);

print "File renaming complete.\n";