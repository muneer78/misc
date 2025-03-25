#!/usr/bin/perl
use LWP::Simple;
use HTML::TokeParser;
use Data::Dumper;

open(FH, "link.txt");
my @filecontent=<FH>;
close FH;

open(HANDLE, ">filecontents.html");

foreach my $url(@filecontent){

print "Fetching content for url: $url \n\n";

my $content = get($url);

open(WH,">temp");
print WH $content;
close WH;

my $tp=HTML::TokeParser->new("temp");
$tp->empty_element_tags(1);
my $content_story="";
	while (my $token=$tp->get_token){
		if(($token->[0] eq"S")&&($token->[1] eq"section")&&($token->[2]{class} eq"body")){
			while(my $token=$tp->get_token){
				if(($token->[0] eq"E")&&($token->[1] eq"section")){
					last;
				}
				if(($token->[0] eq"S")&&($token->[1] eq"footer" || $token->[1] eq"em" || $token->[1] eq"form")){
	    				while($token=$tp->get_token){
	      				       if(($token->[0] eq"E")&&($token->[1] eq"footer" || $token->[1] eq"em" || $token->[1] eq"form")){
							last;
	     					 }
	   				 }
	 			}
				if($token->[0] eq "T"){
       				 $content_story.=$token->[1];
     				}
    				 if($token->[0] eq "S"){
				 $content_story.=$token->[4];
    				 }
    				 if($token->[0] eq "E"){
    				  $content_story.=$token->[2];
   				 }
			}
		}
		
	}
my $contents= $content_story;
print HANDLE $contents;
}
close HANDLE;
