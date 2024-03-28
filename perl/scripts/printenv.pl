#!/usr/bin/perl

# print environment variables
my @keys = keys %ENV;
my @values = values %ENV;
while (@keys) {
    print pop(@keys), '=', pop(@values), "\n";
}