#! /usr/bin/env perl
use strict;
use warnings;
 
my $output = 'output.txt';
open(my $fh, '>', $output) or die "Could not open file '$output' $!";
print $fh "Test Output\n";
close $fh;
print "Test script complete";