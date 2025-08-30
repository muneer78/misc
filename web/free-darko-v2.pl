#!/usr/bin/perl
use strict;
use warnings;
use LWP::UserAgent;
use HTML::TokeParser;
use Data::Dumper;

# Set up user agent
my $ua = LWP::UserAgent->new;
$ua->agent("Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)");

# Open output file to store fetched content
open(my $handle, '>', "totalContent.html") or die "Could not open totalContent.html: $!";

# Fetch content for each year and month
foreach my $year (2005..2011) {
    foreach my $month (1..12) {
        $month = sprintf("%02d", $month);

        # Define the URL
        my $url = "http://freedarko.blogspot.in/${year}_${month}_01_archive.html";
        print "Fetching content for article: $url\n\n";

        # Make HTTP request
        my $res = fetch_url_content($url);
        next unless $res && $res->is_success;

        # Parse and extract post content
        my $content = parse_content($res->content);
        print $handle $content if $content;

        # End parser if last specific date is reached
        last if $year == 2011 && $month == 4;
    }
}

close $handle;

# Fetch the content of the given URL
sub fetch_url_content {
    my ($url) = @_;
    my $req = HTTP::Request->new(GET => $url);
    $req->content_type('application/x-www-form-urlencoded');
    return $ua->request($req);
}

# Parse the HTML content and extract posts by "Bethlehem Shoals"
sub parse_content {
    my ($html_content) = @_;
    my $content = "";

    open(my $temp, '>', "temp") or die "Could not open temp file: $!";
    print $temp $html_content;
    close $temp;

    my $parser = HTML::TokeParser->new("temp");
    $parser->empty_element_tags(1);

    while (my $token = $parser->get_token) {
        # Locate the start of a post div
        if ($token->[0] eq "S" && $token->[1] eq "div" && $token->[2]{class} eq "post") {
            my $post = extract_post($parser);
            $content .= $post if $post;
        }
    }
    return $content;
}

# Extract individual post content if authored by "Bethlehem Shoals"
sub extract_post {
    my ($parser) = @_;
    my $post = "<div class='post'>";
    my $div_counter = 1;
    my $is_by_bs = 0;

    while (my $token = $parser->get_token) {
        # Manage nested divs
        $div_counter++ if $token->[0] eq "S" && $token->[1] eq "div";
        $div_counter-- if $token->[0] eq "E" && $token->[1] eq "div";

        # Capture text within the post
        if ($token->[0] eq "T") {
            if ($token->[1] =~ /posted\sby\sBethlehem\sShoals/) {
                $is_by_bs = 1;
                $post .= "posted by Bethlehem Shoals</em></p></div>";
                last;
            } else {
                $post .= $token->[1];
            }
        } elsif ($token->[0] eq "S") {
            $post .= $token->[4];
        } elsif ($token->[0] eq "E") {
            $post .= $token->[2];
        }

        # End of the main div block
        last if $div_counter == 0;
    }

    return $is_by_bs ? $post : "";
}
