#!/usr/bin/perl

# source: https://stackoverflow.com/a/56485762/14745606

use warnings;
use strict;
use feature qw{ say };

my $string = '1..1188,1189..14,14..15';
my $first_pattern = qr/\.\./;
my $second_pattern = qr/,/;

my @integers = split /$first_pattern|$second_pattern/, $string;
say for @integers;