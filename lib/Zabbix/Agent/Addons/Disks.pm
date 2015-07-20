package Zabbix::Agent::Addons::Disks;

use strict;
use warnings;

# Return an array of block devices, skip if size == 0
sub list_block_dev {
  my @bd = ();
  opendir(my $dh, "/sys/block") or die "Couldn't open /sys/block: $!";
  my @blocks = grep { $_ !~ m/^\./ } readdir($dh);
  closedir($dh);
  foreach my $block (@blocks){
    my $size = 1;
    if ( -e "/sys/block/$block/size"){
      open SIZE, "/sys/block/$block/size";
      $size = join "", <SIZE>;
      close SIZE;
      chomp($size);
      next if ($size eq '0');
    }
    push @bd, $block;
  }
  return @bd;
}

sub list_smart_hdd{
  my ($param) = shift || {};
  my @shd = ();
  if (-x "/usr/sbin/smartctl"){
   foreach my $block (list_block_dev()){
      # Skip block we already know won't support SMART
      next if ($block =~ m/^(ram|loop|md|dm\-)\d+/);
      next unless (system("/usr/sbin/smartctl -A /dev/$block >/dev/null 2>&1") == 0);
      if ($param->{skip_remouvable} && -e "/sys/block/$block/removable"){
        open REMOVABLE, "/sys/block/$block/removable";
        my $removable = join "", <REMOVABLE>;
        close REMOVABLE;
        chomp($removable);
        next if ($removable eq '1');
      }
      push @shd, $block;
    }
  }
  return @shd;
}

1;
