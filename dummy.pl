#!/usr/bin/perl
# print-stuff.pl
use warnings;
use strict;
use Getopt::Std;
use vars qw($opt_w $opt_n);
$|=1;
getopts("wn:");
if ($opt_w) {
  while($opt_w){
    print 'yeah, dogg' . "\r";
    use Time::HiRes qw(sleep);
    sleep(0.25);
    print 'nah, dogg' . "\r";
    use Time::HiRes qw(sleep);
    sleep(0.25);
    print 'hell yeah, playa' . "\r";
    use Time::HiRes qw(sleep);
    sleep(0.25);
    print 'playa please' . "\r";
    use Time::HiRes qw(sleep);
    sleep(0.25);
  }
} elsif ($opt_n) {
for (my $i=0; $i < $opt_n; $i++) {
    print "That's solid\n";
  }
} else {
  print "I have the sads\n";
}
exit(0);