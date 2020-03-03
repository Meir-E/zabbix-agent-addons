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
   BLOCK: foreach my $block (list_block_dev()){
      # Skip block we already know won't support SMART
      next if ($block =~ m/^(ram|loop|md|dm\-)\d+/);
      my $smart_enabled = 0;
      my @smart_info = qx(/usr/sbin/smartctl -i /dev/$block);
      next unless ($? == 0);
      foreach my $line (@smart_info){
        if ($line =~ m/^SMART support is:\s+Enabled/i){
          $smart_enabled = 1;
        } elsif ($line =~ m/^Transport protocol:\s+iSCSI/i){
          # Skip iSCSI block
          next BLOCK;
        }
      }
      # Skip block unless S.M.A.R.T is advertized as enabled
      next unless ($smart_enabled);
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
