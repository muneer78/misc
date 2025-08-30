#!/usr/bin/perl
use strict;
use warnings;
use LWP::Simple;
use HTML::TokeParser;
use Data::Dumper;

# Open the input file containing URLs
open(my $fh, '<', "link.txt") or die "Could not open link.txt: $!";
my @file_content = <$fh>;
close $fh;

# Open the output file to save content
open(my $handle, '>', "filecontents.html") or die "Could not open filecontents.html: $!";

foreach my $url (@file_content) {
    chomp $url;
    print "Fetching content for URL: $url\n\n";

    # Fetch the HTML content from the URL
    my $content = get($url);
    next unless defined $content;

    # Write content to a temporary file
    open(my $temp, '>', "temp") or die "Could not open temp file: $!";
    print $temp $content;
    close $temp;

    # Parse the HTML content
    my $tp = HTML::TokeParser->new("temp");
    $tp->empty_element_tags(1);
    my $content_story = "";

    while (my $token = $tp->get_token) {
        # Look for the beginning of the main content section
        if ($token->[0] eq "S" && $token->[1] eq "section" && $token->[2]{class} eq "body") {
            $content_story .= extract_section_content($tp);
            last;
        }
    }

    # Print the extracted content to the output file
    print $handle $content_story;
}

close $handle;

# Subroutine to extract the section content
sub extract_section_content {
    my ($tp) = @_;
    my $content = "";

    while (my $token = $tp->get_token) {
        # End of the main content section
        last if $token->[0] eq "E" && $token->[1] eq "section";

        # Skip over specific tags (footer, em, form) and their content
        if ($token->[0] eq "S" && ($token->[1] eq "footer" || $token->[1] eq "em" || $token->[1] eq "form")) {
            skip_to_end($tp, $token->[1]);
            next;
        }

        # Extract and add text content
        if ($token->[0] eq "T") {
            $content .= $token->[1];
        } elsif ($token->[0] eq "S") {
            $content .= $token->[4];
        } elsif ($token->[0] eq "E") {
            $content .= $token->[2];
        }
    }
    return $content;
}

# Subroutine to skip over unwanted tags and their content
sub skip_to_end {
    my ($tp, $tag_name) = @_;
    while (my $token = $tp->get_token) {
        last if $token->[0] eq "E" && $token->[1] eq $tag_name;
    }
}
