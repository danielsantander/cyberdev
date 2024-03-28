- [Perl](#perl)
- [Operators](#operators)
- [Comparing Scalars](#comparing-scalars)
- [RegEx](#regex)
    - [Word Matching](#word-matching)
    - [Split Function](#split-function)
    - [OS Version Detection Example](#os-version-detection-example)
- [Variables](#variables)
    - [Scalar Variables](#scalar-variables)
    - [Array Variables](#array-variables)
        - [Referencing Arrays](#referencing-arrays)
    - [Hash Variables](#hash-variables)
        - [Referencing Hashes](#referencing-hashes)
    - [Variable Context](#variable-context)
- [Conditionals](#conditionals)
    - [Conditional Operator](#conditional-operator)
- [Functions or Subroutines](#functions-or-subroutines)
- [Loops](#loops)
- [sources](#sources)
---
# Perl

> This doc assumes version of Perl being used is >= 5

Shebang

```perl
#!/usr/bin/perl
```

Set variable undefined if arg not passed:

```perl
sub my_function
{
    my $key = (@_ == 1) ? shift : undef;
    my %args = @_;
    if(!$args{"foo"})
    {
        $args{"foo"} = "bar";
    }

    # print args
    print "\nargs:\n";
    print "$_ => $args{$_}\n" for (sort keys %args);
    print "\n";
    
    # asking for a particular element, just return the value
    my %hash = ('John Paul', 45, 'Lisa', 30, 'Kumar', 40);
    if($key)
    {
        if (%hash && $hash{$key}) {
            return $hash{$key};
        }
        return undef;
    }
}

# my_function("Lisa") -> OUTPUTS: 30
```

# Operators

[src](https://www.tutorialspoint.com/perl/perl_operators.htm)

# Comparing Scalars

[src](https://www.geeksforgeeks.org/perl-comparing-scalars/)

| Numeric | String | Description                    |
|---------|--------|--------------------------------|
| ==      |  eq    | Equals to                      |
| !=      |  ne    | Not Equals to                  |
| <       |  lt    | Is less than                   |
| >       |  gt    | Is greater than                |
| <=      |  le    | Is less than or equal to       |
| >=      |  ge    | Is greater than or equal to    |

# RegEx

Source:
- [Regular Expressions](https://perldoc.perl.org/perlre)
- [Binding Operators](https://perldoc.perl.org/perlop#Binding-Operators)
- [The Basics](https://perldoc.perl.org/perlretut#Part-1:-The-basics)

## Word Matching

```perl
"Hello World" =~ /World/;  # matches
```

## Split Function

[src](https://perldoc.perl.org/perlretut#The-split-function)

Usage: `split /Pattern/, Expression, Limit`

```perl
# EXAMPLE 1
$text = "Calvin and Hobbes";
@words = split /\s+/, $text;  # $word[0] = 'Calvin'
                              # $word[1] = 'and'
                              # $word[2] = 'Hobbes'

# EXAMPLE 2:
$x = "/usr/bin/perl";
@dirs = split m!/!, $x;     # $dirs[0] = ''
                            # $dirs[1] = 'usr'
                            # $dirs[2] = 'bin'
                            # $dirs[3] = 'perl'

@parts = split m!(/)!, $x;  # $parts[0] = ''
                            # $parts[1] = '/'
                            # $parts[2] = 'usr'
                            # $parts[3] = '/'
                            # $parts[4] = 'bin'
                            # $parts[5] = '/'
                            # $parts[6] = 'perl'
```

## OS Version Detection Example

Use regex to match and retrieve OS version values.

```perl
my $word = "OS version 1.2.3";
my $version = undef;

my $regex = '(?:OS|operating-system|operating system)\sversion';    # (?:) -> non-captured group
my $match = $word =~ /$regex/;  # match -> 1

if ($match){
    my @results = split(/$regex[^0-9]*(\d+\.\d+\.\d+)*/, $word);    # () capture version numbers
    my $result_count = @results;    # 2
    $version = $results[1];         # 1.2.3
}
return $version
```

# Variables

[src](https://www.tutorialspoint.com/perl/perl_variables.htm)

Perl has three basic data types:
1. Scalars -- precede by a dollar sign (`$`) which can store either a number, a string, or a reference.
2. Arrays -- precede by sign `@` and it will store ordered lists of scalars
3. Hashes -- precede by signe `%` and stores sets of key/value pairs.

## Scalar Variables

A Scalar variable is an integer number, floating point, a character, a string, a paragraph, or an entire web page. Simply saying it could be anything, but only a single thing.
```perl
#!/usr/bin/perl

$age = 25;             # An integer assignment
$name = "John Paul";   # A string
$salary = 1445.50;     # A floating point

print "Age = $age\n";
print "Name = $name\n";
print "Salary = $salary\n";

# OUTPUTS:
# Age = 25
# Name = John Paul
# Salary = 1445.5
```

## Array Variables

An array variable stores an ordered list of scalar variables.

```perl
#!/usr/bin/perl

@ages = (25, 30, 40);
@names = ("John Paul", "Lisa", "Kumar");

print "\$ages[0] = $ages[0]\n";
print "\$ages[1] = $ages[1]\n";
print "\$ages[2] = $ages[2]\n";
print "\$names[0] = $names[0]\n";
print "\$names[1] = $names[1]\n";
print "\$names[2] = $names[2]\n";
```

> can reverse order of array with `my @reversearray = reverse @array`

### Referencing Arrays

```perl
# reference arrays with `\@`
@array = (0,1,2,3);     # 0 1 2 3 4 5
$arrayref = \@array;    # ARRAY(0x7fe66e00bf48)

# using a reference to array as an array:
@{$arrayref};           # 0 1 2 3 4 5

# reverse array
reverse @array          # 5 4 3 2 1 0
reverse @{$arrayref}    # 5 4 3 2 1 0

# assign element
$array[3] = 18;
${$arrayref}[3] = 18;

# get element of array
$array[3]        # 18
${$arrayref}[3]  # 18
$arrayref->[3]   # 18

# loop over an array:
for my $element (@array) {
    ...
}

# loop over an array from a reference:
for my $element (@{$arrayref}) {
  ...
}
```

### Multi-Dimensional Arrays

```perl
# 2D array with three elements
@two_d_array = ( [1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]
               );
$two_dim_array[1]->[2]  # 6
$two_dim_array[1][2]    # 6

# 3D array
@three_d_array = ( [
                        [1, 2, 3],
                        [4, 5, 6],
                    ],
                    [
                        [7, 8, 9],
                        [10, 11, 12]
                    ]
                 );
$three_d_array[1]->[1]->[0] # 10
$three_d_array[1][1][0]     # 10
```
## Hash Variables

A hash variable is a set of key/value pairs.

```perl
#!/usr/bin/perl

%data = ('John Paul', 45, 'Lisa', 30, 'Kumar', 40);

print "\$data{'John Paul'} = $data{'John Paul'}\n";
print "\$data{'Lisa'} = $data{'Lisa'}\n";
print "\$data{'Kumar'} = $data{'Kumar'}\n";

# output hash:
print "@{[%data]}"; # Lisa 30 Kumar 40 John Paul 45
print "$_ => $data{$_}\n" for (sort keys %data);
```

### Referencing Hashes

```perl
my %hash = ('John Paul', 45, 'Lisa', 30, 'Kumar', 40);
my $hashref = \%hash;
my $hashkeys = keys %hash;              # 3
my $hashkeysref = keys %{$hashref};     # 3

# assign element
$hash{'Lisa'} = 18;
${$hashref}{'Lisa'} = 18;

# get element from hash
$hash{'Lisa'};         # 18
${$hashref}{'Lisa'};   # 18
$hashref->{'Lisa'};    # 18

# print contents of hash:
for my $key (keys %hash) {
    print "$key => $hash($key)\n";
}

# print contents of hash reference:
for my $key (keys %{$hashref}) {
    print "$key => $hashref{$key}\n";
}
```

## Variable Context

Perl treats same variable differently based on Context, i.e., situation where a variable is being used.

```perl
#!/usr/bin/perl

@names = ('John Paul', 'Lisa', 'Kumar');
@copy = @names;
$size = @names;

print "Given names are : @copy\n";
print "Number of names are : $size\n";

# OUTPUTS:
# Given names are : John Paul Lisa Kumar
# Number of names are : 3
```

# Conditionals

[src](https://www.tutorialspoint.com/perl/perl_conditions.htm)

|STATEMENT                      | DESCRIPTION                                                                           |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
|if statement                   | An if statement consists of a boolean expression followed by one or more statements.                                                                           |
|if...else statement            | An if statement can be followed by an optional else statement.                                                                                                 |
|if...elsif...else statement    | An if statement can be followed by an optional elsif statement and then by an optional else statement.                                                         |
|unless statement               | An unless statement consists of a boolean expression followed by one or more statements.                                                                       |
|unless...else statement        | An unless statement can be followed by an optional else statement.                                                                                             |
|unless...elsif..else statement | An unless statement can be followed by an optional elsif statement and then by an optional else statement.                                                     |
|switch statement               | With the latest versions of Perl, you can make use of the switch statement. which allows a simple way of comparing a variable value against various conditions.|


## Conditional Operator

Shorthand version of `if...else` statements. Usage: `Exp1 ? Exp2 : Exp3;`

```perl
#!/usr/local/bin/perl
 
$name = "Ali";
$age = 10;
$status = ($age > 60 ) ? "A senior citizen" : "Not a senior citizen";
print "$name is  - $status\n";

# OUTPUT:
# Ali is - Not a senior citizen
```

# Functions or Subroutines

```perl
sub subroutine_name
{
    # body of method or subroutine
}

# call the subroutine with:
subroutine_name(arguments_list)
```

## Passing Arguments

Pass arguments to subroutines.

```perl
#!/usr/bin/perl 

sub area
{ 
    # passing argument     
    $side = $_[0]; 
    return ($side * $side); 
} 
  
# calling function 
$totalArea = area(4); 
  
# displaying result 
printf $totalArea; 

# OUTPUTS:
# 16
```

# Loops

```perl
foreach ( 1, 3, 7 ) {
    print "\$_ is $_";
}

# or
my @numbers = ( 1, 3, 7 );
foreach ( @numbers ) {
    print "\$_ is $_";
}
```

Print environment variables:

```perl
my @keys = keys %ENV;
my @values = values %ENV;
while (@keys) {
    print pop(@keys), '=', pop(@values), "\n";
}
```

# sources

- [perldoc -- Using References](https://perldoc.perl.org/perlreftut#Using-References)