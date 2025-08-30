#!/usr/bin/perl
use strict;
use warnings;
use LWP::UserAgent;
use HTML::TreeBuilder;
use URI;
use File::Slurp;

# Base URL to start scraping
my $base_url = "https://ludic.mataroa.blog/";
my %visited;
my $output_file = "scraped_output.md";

# Initialize user agent
my $ua = LWP::UserAgent->new;
$ua->timeout(10);

# Open the output file
open(my $fh, '>', $output_file) or die "Could not open file '$output_file' $!";

# Start scraping
scrape_page($base_url);

# Close the file handle
close $fh;

sub scrape_page {
    my ($url) = @_;

    # Skip already visited URLs
    return if $visited{$url};
    $visited{$url} = 1;

    # Fetch the page content
    my $response = $ua->get($url);
    if (!$response->is_success) {
        warn "Failed to fetch $url: " . $response->status_line;
        return;
    }

    my $content = $response->decoded_content;

    # Parse the content with HTML::TreeBuilder
    my $tree = HTML::TreeBuilder->new_from_content($content);
    $tree->elementify;

    # Extract and write page content
    my $body = $tree->look_down(_tag => 'body');
    if ($body) {
        # Extract and preserve full HTML content within <body>
        my $html_content = $body->as_HTML('<>&', ' ', {});
        print $fh "### Page URL: $url\n\n";
        print $fh $html_content . "\n\n---\n\n";
    } else {
        warn "No <body> content found on $url\n";
    }

    # Extract links
    my @links = $tree->find_by_tag_name('a');
    foreach my $link (@links) {
        my $href = $link->attr('href');
        next unless $href;

        # Make absolute URL
        my $abs_url = URI->new_abs($href, $url)->as_string;

        # Only process internal links
        if ($abs_url =~ /^\Q$base_url\E/) {
            scrape_page($abs_url);
        }
    }

    $tree->delete; # Free memory
}
