#!/usr/bin/perl

# script for converting BPASS v2.0 and v2.1 tarballs to Cloudy ascii files
# written by Peter van Hoof with modifications by Jane Rigby.

use warnings;
use strict;
use IO::Zlib;
use Cwd;

my $dir = getcwd;
$dir =~ s#^.*/##;
my $nAge;

if( -d "OUTPUT_CONT" && -d "OUTPUT_POP" ) {
    # this branch is for v2.0
    $nAge = 41;
    &convert_single( "OUTPUT_CONT", "single", "$dir" . "_cont_single.ascii" );
    &convert_single( "OUTPUT_CONT", "binary", "$dir" . "_cont_binary.ascii" );
    &convert_single( "OUTPUT_POP",  "single", "$dir" . "_burst_single.ascii" );
    &convert_single( "OUTPUT_POP",  "binary", "$dir" . "_burst_binary.ascii" );
}
else {
    # this branch is for v2.1+
    $nAge = 51;
    &convert_single( ".", "single", "$dir" . "_burst_single.ascii" );
    &convert_single( ".", "binary", "$dir" . "_burst_binary.ascii" );
}

sub convert_single
{
    my $subdir = shift;
    my $evol = shift;
    my $outnam = shift;
    $outnam =~ s/v2\./v2p/;  # extra dot in filename only works from c17.01 onwards, so fix it here
    my @logZ;
    my @Age;
    my $nZ = 0;

    print "Creating $outnam\n";
    #Correction works for binary pop
    my $wildcard = ( $evol eq "single" ) ? "$subdir/spectra.z*.gz" : "$subdir/spectra-bin*.gz";

    while( my $input = glob("$wildcard") ) {
	my @field = split( /\./, $input );
	for( my $i=0; $i <= $#field; ++$i ) {
	    if( $field[$i] =~ /^z/ ) {
		$field[$i] =~ s/^z//;
		my $Z;
		if( $field[$i] eq "em4" ) {
		    $Z = 1.0e-4;
		}
		elsif( $field[$i] eq "em5" ) {
		    $Z = 1.0e-5;
		}
		else {
		    $Z = $field[$i]/1000.;
		}
		$logZ[$nZ] = log($Z)/2.302585092994045684017991;
	    }
	}
	++$nZ;
    }
    my $nmod = $nZ * $nAge;
    my $nlin = 100000;
    for( my $i=0; $i < $nAge; ++$i ) {
	$Age[$i] = 10.**(6. + $i/10.);
    }

    open( my $out, ">", "$outnam" ) or die "Can't open $outnam\n";

    print $out "  20060612\n";
    print $out "  2\n";
    print $out "  2\n";
    print $out "  Age\n";
    print $out "  log(Z)\n";
    print $out "  $nmod\n";
    print $out "  $nlin\n";
    print $out "  lambda\n";
    print $out "  1.00000000e+00\n";
    print $out "  F_lambda\n";
    print $out "  1.00000000e+00\n";
    my $n = 0;
    for( my $i=0; $i < $nZ; ++$i ) {
 	for( my $j=0; $j <= $#Age; ++$j ) {
	    print $out "  $Age[$j] $logZ[$i]";
	    ++$n;
	    if( ($n%2) == 0 ) {
		print $out "\n";
	    }
	}
    }
    if( ($n%2) != 0 ) {
	print $out "\n";
    }

    my $nf = 0;
    while( my $input = glob("$wildcard") ) {
	print( "  processing $input...\n" );
	my $in = new IO::Zlib;
	$in->open( "$input", "rb" );
	my @output;
	$n = 0;
	while( <$in> ) {
	    ++$n;
	    chomp;
	    s/^ +//;
	    s/ +$//;
	    my @field = split( / +/ );
	    if( $#field != $nAge ) {
		die "Internal error: wrong number of fields in input file.";
	    }
	    for( my $i=0; $i <= $nAge; ++$i ) {
		if( $field[$i] >= 0. ) {
		    $output[$i] .= "  $field[$i]";
		}
		else {
		    print "negative flux lambda=$field[0] age=$Age[$i-1] $field[$i] set to zero\n";
		    $output[$i] .= "  0.0000000E+00";
		}
		if( ($n%5) == 0 ) {
		    $output[$i] .= "\n";
		}
	    }
	}
	if( $n != $nlin ) {
	    die "Internal error: wrong number of wavelength points.";
	}
	if( $nf == 0 ) {
	    print $out $output[0];
	}
	for( my $i=1; $i <= $nAge; ++$i ) {
	    print $out $output[$i];
	}
	++$nf;
	$in->close;
    }

    close( $out );
}

