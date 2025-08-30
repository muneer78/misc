#!/usr/bin/perl
use LWP::UserAgent;
use HTML::TokeParser;
use Data::Dumper;

my $ua = LWP::UserAgent->new;
$ua->agent("Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)");

open(HANDLE, ">totalContent.html");

foreach my $year(2005..2014){
	foreach my $month(1..12){
	$month = sprintf("%02d", $month);
	
	my $url="http://gangrey.com/?m=".$year.$month;
	my $req = HTTP::Request->new(GET => $url);
	$req->content_type('application/x-www-form-urlencoded');
	my $res = $ua->request($req);
	
	my $article="";
		if ($res->is_success) {
		open(WH,">temp");
		print WH $res->content;
		close WH;

		my $tp=HTML::TokeParser->new("temp");
		$tp->empty_element_tags(1);
		my $url="";

		while(my $token=$tp->get_token){
			if(($token->[0] eq "S")&&($token->[1] eq "article")){
				while(my $token=$tp->get_token){
					if(($token->[0] eq "E")&&($token->[1] eq "article")){
						last;
					}						
					if($token->[0] eq "T"){
						$article.=$token->[1];
	     				}
	    				if($token->[0] eq "S"){
		 				$article.=$token->[4];
	    				}
	    				if($token->[0] eq "E"){
	   					$article.=$token->[2];
					}
				}
			}#start article
		}##while
		}##if success
	 
		print HANDLE $article;
	
   	
	}
}
close HANDLE;
