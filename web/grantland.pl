#!/usr/bin/perl

use strict;
use warnings;
use WWW::Mechanize;
use URI::Extract;

# Configure Mechanize
my $mech = WWW::Mechanize->new(autocheck => 1);
$mech->user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36');

# Base URL for features section
my $base_url = 'https://grantland.com/features';

# Get the features page
$mech->get($base_url);

# Extract all links from the features page
my @links = $mech->links(rel => '');

# Filter for links within the features section
my @subpages = grep { $_->url =~ /^$base_url\// } @links;

foreach my $link (@subpages) {
  # Extract the URL and filename
  my $url = $link->url;
  my $filename = basename($url);

  # Skip non-HTML files
  next unless $filename =~ /\.html/;

  # Download the subpage content
  $mech->get($url);
  my $content = $mech->content;

  # Remove unnecessary HTML elements (adjust selectors as needed)
  $content =~ s/<(script|style|header|footer|nav).*?>.*?<\/\1>//gs;

  # Convert HTML to basic Markdown (consider using external tools for better conversion)
  $content =~ s/<h1>(.*?)<\/h1>/# $1\n/gs;
  $content =~ s/<h2>(.*?)<\/h2>/## $1\n/gs;
  $content =~ s/<h3>(.*?)<\/h3>/### $1\n/gs;
  $content =~ s/<p>(.*?)<\/p>/\\n$1\n\\n/gs;
  $content =~ s/<strong>(.*?)<\/strong>/\*\1\* /gs;
  $content =~ s/<em>(.*?)<\/em>/_$1_/gs;

  # Save the content to a markdown file
  open(my $fh, '>', "features/$filename.md") or die "Error opening file: $!";
  print $fh $content;
  close $fh;

  print "Saved: $filename.md\n";
}