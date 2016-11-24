package Zabbix::Agent::Addons::UPS;

use warnings;
use strict;
use File::Which;
use File::Spec;
open STDERR, '>', File::Spec->devnull() or die "could not open STDERR: $!\n";

# List configured UPS (only nut is supported)
sub list_ups {
  my @ups = ();
  my $upsc = which('upsc');
  if ($upsc && -x $upsc){
    my @out = qx($upsc -l);
    if ($? == 0){
      @ups = @out;
      chomp @ups;
    }
  }
  return @ups;
};

1;
