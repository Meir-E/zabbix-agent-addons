%if 0%{?rhel} && 0%{?rhel} < 7
%global _without_selinux 1
%endif

Summary: Scripts for Zabbix monitoring
Name: zabbix-agent-addons
Version: 0.2.138
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

License: GPL
Group: Virtualization
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Requires: zabbix-agent
Requires: perl(Getopt::Long)
Requires: perl(Getopt::Std)
Requires: perl(JSON)
Requires: perl(POSIX)
Requires: perl(MIME::Base64)
Requires: perl(File::Which)
Requires: perl(Config::Simple)
Requires: perl(Statistics::Descriptive)
Requires: fping
BuildRequires: perl
%if ! 0%{?_without_selinux}
Requires: policycoreutils
BuildRequires: selinux-policy-devel
BuildRequires: checkpolicy
%endif

AutoReqProv: no

%description
This package contains some usefull script to monitor
a Linux box with Zabbix. It provides helper scripts to
discover and monitor things like filesystems, block devices
LVM, RAID status, S.M.A.R.T. drives, BackupPC etc...

%prep
%setup -q

%build
%if ! 0%{?_without_selinux}
pushd selinux
make -f %{_datadir}/selinux/devel/Makefile
popd
%endif

%install

%{__rm} -rf $RPM_BUILD_ROOT

# Install zabbix scripts
%{__install} -d -m 750 $RPM_BUILD_ROOT%{_localstatedir}/lib/zabbix/bin
%{__install} -m 0755 zabbix_scripts/* $RPM_BUILD_ROOT%{_localstatedir}/lib/zabbix/bin
# Install Zabbix conf
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.conf.d/
%{__install} -m 0644 zabbix_conf/* $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.conf.d/
# Install perl modules
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{perl_vendorlib}
cp -r lib/* $RPM_BUILD_ROOT%{perl_vendorlib}/
# Install sensors conf
%{__install} -m 0755 conf/sensors.ini $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/
# Install sudo conf
%{__install} -d 750 $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d
%{__install} -m 600 conf/sudo.conf $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d/zabbix_agent
# Install SELinux policy
%if ! 0%{?_without_selinux}
%{__install} -d 750 $RPM_BUILD_ROOT%{_datadir}/selinux/packages/%{name}
%{__install} -m644 selinux/%{name}.pp $RPM_BUILD_ROOT%{_datadir}/selinux/packages/%{name}/%{name}.pp
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre


%preun

%post
if [ $1 -eq 2 ] ; then
  if [ -e "/etc/zabbix/sensors.conf" ]; then
    /var/lib/zabbix/bin/util_convert_sensors_ini /etc/zabbix/sensors.conf
  fi
fi

%files
%defattr(-,root,root,-)
%doc README
%doc zabbix_templates/*
%dir %attr(0750,zabbix,zabbix) %{_localstatedir}/lib/zabbix/bin
%{_localstatedir}/lib/zabbix/bin/*
%{perl_vendorlib}
%config(noreplace) %attr(0640,root,zabbix) %{_sysconfdir}/zabbix/sensors.ini
%config(noreplace) %attr(0640,root,zabbix) %{_sysconfdir}/zabbix/zabbix_agentd.conf.d/*
%attr(0440,root,root) %{_sysconfdir}/sudoers.d/*
%if ! 0%{?_without_selinux}
%{_datadir}/selinux/packages/%{name}/%{name}.pp
%endif

%changelog
* Mon Jan 11 2021 Daniel Berteaud <daniel@firewall-services.com> 0.2.138-1
- Add missing Samba application name for aggregated items (daniel@firewall-
  services.com)
- Minor fixes for samba script and template (daniel@firewall-services.com)

* Sat Jan 09 2021 Daniel Berteaud <daniel@firewall-services.com> 0.2.137-1
- Add scripts and template to monitor Samba 4 DC (daniel@firewall-services.com)

* Fri Jan 08 2021 Daniel Berteaud <daniel@firewall-services.com> 0.2.136-1
- Add guest counter for PVE cluster and node (daniel@firewall-services.com)

* Thu Dec 17 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.135-1
- Update Template_App_MySQL (daniel@firewall-services.com)
- Update Template_App_ZFS (daniel@firewall-services.com)

* Tue Dec 01 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.134-1
- Possibility to check certificate for Unifi API (daniel@firewall-services.com)

* Sat Nov 07 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.133-1
- Add perl in BuildReq for el8 (daniel@firewall-services.com)

* Mon Oct 26 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.132-1
- Run upsc commands with 2>/de/null (daniel@firewall-services.com)
- IPMI sensors can have / and - in their name (daniel@firewall-services.com)

* Thu Oct 22 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.131-1
- Don't return garbage in mpath discovery if command failed (daniel@firewall-
  services.com)

* Tue Oct 20 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.130-1
- Add App_Multipath template (daniel@firewall-services.com)
- Add Linux_Server template (daniel@firewall-services.com)

* Tue Oct 20 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.129-1
- Add scripts to discover and check multipath devices (daniel@firewall-
  services.com)

* Tue Sep 29 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.128-1
- Use MAC of device if no name is defined in Unifi device discovery
  (daniel@firewall-services.com)

* Wed Sep 23 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.127-1
- Update scripts to work with ssacli (in adition to hpacucli) (daniel@firewall-
  services.com)

* Fri Sep 04 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.126-1
- Add some compatibility for older MySQL servers (daniel@firewall-services.com)

* Tue Sep 01 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.125-1
- Allow empty --defaults opt for check_mysql_sudo (daniel@firewall-
  services.com)

* Mon Aug 31 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.124-1
- Update Template_App_MySQL (daniel@firewall-services.com)

* Mon Aug 31 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.123-1
- check_mysql needs sudo permissions (daniel@firewall-services.com)

* Mon Aug 31 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.122-1
- Add MySQL monitoring script and template (daniel@firewall-services.com)
- Add Template_Vhost (daniel@firewall-services.com)
- Add templates for Windows (minimal and server) (daniel@firewall-services.com)
- Add /usr/local/BackupPC/lib as lib dir for BackupPC scripts (daniel@firewall-
  services.com)

* Wed May 20 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.121-1
- Do not rely on distrib version to check if --output-format is needed for
  check_pve_sudo (daniel@firewall-services.com)

* Fri Apr 03 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.120-1
- Fix mdadm when we have spares (daniel@firewall-services.com)

* Tue Mar 03 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.119-1
- Better detection of smart capable drives (daniel@firewall-services.com)

* Mon Mar 02 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.118-1
- Update Template_App_PVE_Cluster (daniel@firewall-services.com)

* Mon Mar 02 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.117-1
- Add basic SNMP templates (daniel@firewall-services.com)
- Add Template_App_Unifi (daniel@firewall-services.com)
- Add Template_OS_PfSense2 (daniel@firewall-services.com)
- Add Template_Ping (daniel@firewall-services.com)
- Fix cache when the same resource is queried with different options
  (daniel@firewall-services.com)
- Remove debug statement in util_populate_pve_cache (daniel@firewall-
  services.com)

* Mon Mar 02 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.116-1
- Default to accept cached value up to 5 min old for check_pve_sudo
  (daniel@firewall-services.com)

* Mon Mar 02 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.115-1
- Add a script to populate check_pve_sudo cache (daniel@firewall-services.com)
- Enhance check_pve_sudo with a local cache support to speed up monitoring
  (daniel@firewall-services.com)

* Tue Feb 25 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.114-1
- Automatic commit of package [zabbix-agent-addons] release [0.2.112-1].
  (daniel@firewall-services.com)
- drop stderrr for upsc commands (daniel@firewall-services.com)

* Tue Feb 25 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.113-1
- Skip Core X temp sensors (daniel@firewall-services.com)

* Wed Feb 19 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.112-1
- drop stderrr for upsc commands (daniel@firewall-services.com)

* Mon Feb 17 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.111-1
- Update ZFS and BackupPC templates (daniel@firewall-services.com)

* Mon Feb 10 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.110-1
- Fix a typo in ZabbixSizeTooSmallFactor conf (daniel@firewall-services.com)

* Wed Feb 05 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.109-1
- Don't skip local node in PVE nodes discovery (daniel@firewall-services.com)

* Wed Jan 22 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.108-1
- Only skip RAID volumes checks when in HBA mode, not physical disks checks
  (daniel@firewall-services.com)
- Declar variable in the correct scope for hba mode detection (daniel@firewall-
  services.com)
- Handle megaraid controlers in HBO/JBOD mode (skip RAID checks)
  (daniel@firewall-services.com)
- Use head -1 to be sure to get a single value for sensors (daniel@firewall-
  services.com)

* Thu Jan 16 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.107-1
- Add Zabbix template for Squid (daniel@firewall-services.com)

* Thu Jan 16 2020 Daniel Berteaud <daniel@firewall-services.com> 0.2.106-1
- Remove uri from UsereParam args for squid (daniel@firewall-services.com)

* Tue Dec 17 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.105-1
- Fix ready sizeNew from last backup (except when link hasn't ran yet)
  (daniel@firewall-services.com)

* Sun Dec 15 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.104-1
- Disable vfs.dev.discovery in default conf (daniel@firewall-services.com)

* Sun Dec 15 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.103-1
- Set min backup size to 0 in template (daniel@firewall-services.com)

* Sun Dec 15 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.102-1
- Fix key name for enabled value (daniel@firewall-services.com)

* Sun Dec 15 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.101-1
- Init complete JSON objects with default values in bheck_backuppc_sudo
  (daniel@firewall-services.com)
- Remove unused variables (daniel@firewall-services.com)

* Sun Dec 15 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.100-1
- Only substract $new_size_of_last_full once (daniel@firewall-services.com)

* Fri Dec 13 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.99-1
- Fix when a host has a single backup with 0 new file size (daniel@firewall-
  services.com)

* Fri Dec 13 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.98-1
- Fix backups total size computation when there's only one full
  (daniel@firewall-services.com)

* Fri Dec 13 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.97-1
- Include Zabbix template to monitor BackupPC (daniel@firewall-services.com)

* Fri Dec 13 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.96-1
- Enhanced stats for BackupPC's entity (daniel@firewall-services.com)

* Wed Dec 11 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.95-1
- Wait for BackupPC_link to run before we take new sizes in our stat
  (daniel@firewall-services.com)

* Wed Dec 11 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.94-1
- Fix BackupPC script when BackuPPC_link is waiting for the nightly cleanup to
  finish (daniel@firewall-services.com)

* Fri Nov 29 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.93-1
- Don't use autoloader in our forked Linux::LVM (daniel@firewall-services.com)
- Don't requires Linux::LVM anymore (daniel@firewall-services.com)
- Replace Linux::LVM occurrences with Zabbix::Agent::Addons::LVM
  (daniel@firewall-services.com)
- Bundle a fork of Linux::LVM with support for LVM thin pools (daniel@firewall-
  services.com)

* Wed Nov 27 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.92-1
- Better compat with 4.4 vfs.dev.discovery (and use lsblk to get the list of
  dev if available) (daniel@firewall-services.com)

* Tue Nov 26 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.91-1
- Add DEVNAME macro for vfs.dev.discovery to ease transition to 4.4
  (daniel@firewall-services.com)
- Minor update in ZFS template (daniel@firewall-services.com)

* Sun Oct 20 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.90-1
- Fix some unifi stats for uap/usw in recent unifi versions (daniel@firewall-
  services.com)

* Mon Oct 14 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.89-1
- Add Zabbix template for GlusterFS (daniel@firewall-services.com)
- Add Zabbix tempalte for DRBD (daniel@firewall-services.com)
- Add Zabbix template for Proxmox Mail Gateway (daniel@firewall-services.com)
- Add template to monitor a PVE cluster (daniel@firewall-services.com)
- ZFS ARC low hit ratio for data and global are calculated for 1h
  (daniel@firewall-services.com)

* Fri Oct 11 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.88-1
- Add Zabbix template for ZFS (daniel@firewall-services.com)

* Fri Oct 11 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.87-1
- Enhance ZFS monitoring scripts to retrieve ARC stats (daniel@firewall-
  services.com)
- Send an empty data array when Zimbra is not installed (daniel@firewall-
  services.com)

* Tue Oct 01 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.86-1
- Fix pve script when no net or disk stats are available (daniel@firewall-
  services.com)

* Sat Sep 21 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.85-1
- Check $sanoidmon is defined before checking its value (daniel@firewall-
  services.com)

* Sat Sep 21 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.84-1
- Fix var name in disco_zfs (daniel@firewall-services.com)

* Sat Sep 21 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.83-1
- Better sanoïd monitoring integration (daniel@firewall-services.com)

* Fri Sep 20 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.82-1
- Remove trailing x for compressratio with ZoL < 0.8 (daniel@firewall-
  services.com)

* Fri Sep 20 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.81-1
- Revert to suffix conversion for ZFS error count (daniel@firewall-
  services.com)

* Fri Sep 20 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.80-1
- Rewrite ZFS monitoring from scratch (daniel@firewall-services.com)
- Set info in the data element for Zimbra discovery (daniel@firewall-
  services.com)

* Fri Sep 13 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.79-1
- Add simple Zabbix service status scripts (daniel@firewall-services.com)

* Tue Sep 03 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.77-1
- Skip self PVE node (daniel@firewall-services.com)

* Tue Jul 30 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.76-1
- Add support for some NVMe temp sensors Found on OVH's Advanced servers for
  example (daniel@firewall-services.com)
- Fix when running on Debian buster Which fails with RC 25 when using
  File::Spec devnull (daniel@firewall-services.com)

* Tue May 21 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.75-1
- Add basic scripts to monitor VDO volumes (daniel@firewall-services.com)

* Tue Apr 16 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.74-1
- Don't fail if Statistics::Descriptive doesn't support quantile
  (daniel@firewall-services.com)

* Mon Apr 15 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.73-1
- More work on BackupPC's monitoring scripts (daniel@firewall-services.com)

* Thu Apr 04 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.72-1
- Fix reporting MaxXferError (daniel@firewall-services.com)

* Thu Apr 04 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.71-1
- Fix a typo in check_backuppc_sudo (daniel@firewall-services.com)

* Thu Apr 04 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.70-1
- Fix counting entity size (daniel@firewall-services.com)

* Thu Apr 04 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.69-1
- Don't count vm as an entity in BackupPC's entities discovery
  (daniel@firewall-services.com)

* Thu Apr 04 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.68-1
- Update BackupPC's discovery and monitoring scripts (daniel@firewall-
  services.com)

* Wed Apr 03 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.67-1
- Add last_errors in backuppc JSON info (daniel@firewall-services.com)
- Update conf for BackupPC (daniel@firewall-services.com)

* Wed Apr 03 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.66-1
- Remove crazy and useless regex to exclude hosts from BackupPC
  (daniel@firewall-services.com)

* Wed Apr 03 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.65-1
- Enhance backuppc reporting script Including reporting the new file size, and
  sending all the info at once in JSON format (daniel@firewall-services.com)
- Some coding style updates (daniel@firewall-services.com)
- More compact BPCSTATUS (1/0 instead of enabled/disabled) (daniel@firewall-
  services.com)

* Wed Feb 20 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.64-1
- Also report the number in the deferred queue (daniel@firewall-services.com)

* Wed Feb 20 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.63-1
- Report number of email in the active and hold queues (daniel@firewall-
  services.com)

* Sat Jan 19 2019 Daniel Berteaud <daniel@firewall-services.com> 0.2.62-1
- Add scripts to ping other hosts (daniel@firewall-services.com)

* Mon Dec 10 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.61-1
- Save cookies to a file so we don't have to login at every invocation GLPI
  #34449 (daniel@firewall-services.com)

* Sun Dec 09 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.60-1
- Print ZBX_NOTSUPPORTED in case of API error Prevent tons of error messages in
  Zabbix Server's logs (daniel@firewall-services.com)

* Sun Dec 09 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.59-1
- Fix ZBX_NOTSUPPORTED string in several scripts (daniel@firewall-services.com)

* Thu Nov 15 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.57-0.beta1
- Add enhanced squid monitoring support (daniel@firewall-services.com)

* Fri Nov 09 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.56-1
- Add simple script for nginx (similar httpd) (daniel@firewall-services.com)

* Fri Oct 26 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.55-1
- Fix PVE storage monitoring GLPI #33910 (daniel@firewall-services.com)

* Wed Oct 24 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.54-1
- Rework PMG monitoring scripts (daniel@firewall-services.com)

* Thu Oct 18 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.52-0.beta1
- Add very basic script for PMG monitoring (daniel@firewall-services.com)

* Tue Sep 18 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.51-1
- check_unifi: also output satisfaction for stations (daniel@firewall-
  services.com)

* Mon Sep 17 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.50-1
- Fix comparison with uninitialized value in check_unifi (daniel@firewall-
  services.com)

* Sat Sep 15 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.49-1
- Report number of unarchived alarms in check_unifi --unifi (daniel@firewall-
  services.com)

* Sat Sep 15 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.48-1
- More fixes for AP monitoring in check_unifi (daniel@firewall-services.com)

* Sat Sep 15 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.47-1
- Several fixes in check_unifi (daniel@firewall-services.com)

* Fri Sep 14 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.46-1
- Enhance Unifi discovery and monitoring Adding support for station monitoring
  (daniel@firewall-services.com)

* Thu Sep 13 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.45-0.beta2
- Fix check_unifi when value is defined but false (daniel@firewall-
  services.com)

* Thu Sep 13 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.44-0.beta1
- Add scripts to monitor Unifi sites (daniel@firewall-services.com)

* Tue Aug 21 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.43-1
- Fix PVE scripts to Work with new pvesh version (daniel@firewall-services.com)

* Mon Jul 23 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.42-1
- Initialize an empty json object (daniel@firewall-services.com)

* Mon Jul 09 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.41-1
- Don't log sudo usage for Zabbix (daniel@firewall-services.com)

* Wed Jul 04 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.40-1
- Fix ZFS pool stats retrieval (daniel@firewall-services.com)

* Wed Jun 13 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.39-1
- Fix computing pool CPU usage in check_pve (daniel@firewall-services.com)

* Thu Jun 07 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.38-1
- Add global net and disk stats for the cluster in check_pve_sudo
  (daniel@firewall-services.com)

* Tue Jun 05 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.37-1
- Fix check_pve_sudo for single node monitoring (daniel@firewall-services.com)

* Tue Jun 05 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.36-1
- Remove redundant condition (daniel@firewall-services.com)
- Fix {#PVE_STOR_STATUS} macro (daniel@firewall-services.com)
- Only gather info about online nodes (daniel@firewall-services.com)
- Add some global cluster stats for PVE (daniel@firewall-services.com)

* Sun Jun 03 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.35-1
- Enhance PVE scripts and conf (daniel@firewall-services.com)
- Add basic scripts for PVE monitoring (daniel@firewall-services.com)

* Wed May 30 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.34-1
- Add stats for ZFS zpools (daniel@firewall-services.com)

* Tue May 29 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.33-1
- Ensure we always return a value for scan action status errors in check_zfs
  (daniel@firewall-services.com)

* Tue May 29 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.32-1
- Handle situations where there's more than 1000 errors on a item in ZFS pools
  (daniel@firewall-services.com)

* Tue May 29 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.31-1
- Various enhancements in check_zfs (daniel@firewall-services.com)
- Fix macro name for zfs zpool discovery (daniel@firewall-services.com)

* Mon May 28 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.30-1
- Rename vfs.zfs.discovery to vfs.zfs.zpool.discovery So later we'll be able to
  add other discovery rules for say, datasets (daniel@firewall-services.com)

* Mon May 28 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.29-1
- Add scripts to discover and check ZFS zpools (daniel@firewall-services.com)

* Tue Mar 06 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.28-1
- Use "all" key to get all httpd stats in JSON format (daniel@firewall-
  services.com)

* Tue Mar 06 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.27-1
- Respond with all stats as a JSON structure if no --what given
  (daniel@firewall-services.com)

* Tue Mar 06 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.26-1
- Support space in httpd status key So total_accesses and total_kbytes are
  available again (daniel@firewall-services.com)

* Tue Feb 06 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.25-1
- Fix mdadm RAID discovery condition (daniel@firewall-services.com)

* Tue Jan 09 2018 Daniel Berteaud <daniel@firewall-services.com> 0.2.24-1
- Don't WARN when device is being checked, only when it's rebuilding
  (daniel@firewall-services.com)
- Don't detect mdadm RAID in containers (daniel@firewall-services.com)

* Thu Nov 30 2017 Daniel Berteaud <daniel@firewall-services.com> 0.2.23-1
- Check line format in check_httpd Instead of spliting errors in case server-
  status redirect to somewhere else (daniel@firewall-services.com)

* Mon Nov 20 2017 Daniel Berteaud <daniel@firewall-services.com> 0.2.22-1
- Add script to monitor spamassassin's bayes database stats (daniel@firewall-
  services.com)
- Symlink releasrs.conf to global's one (daniel@firewall-services.com)

* Tue Nov 14 2017 Daniel Berteaud <daniel@firewall-services.com> 0.2.21-1
- Remove now non existing CHANGELOG.git file (daniel@firewall-services.com)

* Tue Nov 14 2017 Daniel Berteaud <daniel@firewall-services.com> 0.2.20-1
- new package built with tito

* Thu Oct 12 2017 Daniel Berteaud <daniel@firewall-services.com> - 0.2.19-1
- Correctly handle Partially Degraded state

* Thu Aug 24 2017 Daniel Berteaud <daniel@firewall-services.com> - 0.2.18-1
- Only include SELinux policy module on el7

* Wed Aug 23 2017 Daniel Berteaud <daniel@firewall-services.com> - 0.2.17-1
- Add a SELinux policy module

* Wed Jun 14 2017 Daniel Berteaud <daniel@firewall-services.com> - 0.2.16-1
- Add kernel.openedfile UserParameter

* Thu Nov 24 2016 Daniel Berteaud <daniel@firewall-services.com> - 0.2.15-1
- Fix discovery scripts to always return a valid JSON value, even if empty
  (sensors, lvm and nut_ups)

* Wed Nov 9 2016 Daniel Berteaud <daniel@firewall-services.com> - 0.2.14-1
- Add scripts to monitor apache httpd

* Sun Oct 30 2016 Daniel Berteaud <daniel@firewall-services.com> - 0.2.13-1
- Fix handling Airflow_Temperature_Cel label

* Fri Oct 28 2016 Daniel Berteaud <daniel@firewall-services.com> - 0.2.12-1
- Support Airflow_Temperature_Cel as temp label for smartctl based sensors

* Thu Sep 1 2016 Daniel Berteaud <daniel@firewall-services.com> - 0.2.11-1
- Add support for lm_sensors based sensors

* Thu Aug 25 2016 Daniel Berteaud <daniel@firewall-services.com> - 0.2.10-1
- Add monitoring item for squid's FD

* Wed Apr 6 2016 Daniel Berteaud <daniel@firewall-services.com> - 0.2.9-1
- Detect HDD temp sensors on sat+megaraid controllers

* Mon Mar 21 2016 Daniel B. <daniel@firewall-services.com> - 0.2.8-1
- Prevent running several gluster check commands at the same time

* Wed Sep 16 2015 Daniel B. <daniel@firewall-services.com> - 0.2.7-1
- Prevent GlusterFS heal false positive due to concurrent locking

* Mon Sep 14 2015 Daniel B. <daniel@firewall-services.com> - 0.2.6-1
- Add script to discover and monitor DRBD resources

* Wed Sep 9 2015 Daniel B. <daniel@firewall-services.com> - 0.2.5-1
- Support negative values for temp sensors

* Mon Jul 27 2015 Daniel B. <daniel@firewall-services.com> - 0.2.4-1
- Several enhancements in sensors ini generator

* Fri Jul 24 2015 Daniel B. <daniel@firewall-services.com> - 0.2.3-1
- Separate UPS default threshold
- Minor coding style updates

* Mon Jul 20 2015 Daniel B. <daniel@firewall-services.com> - 0.2.2-1
- Start working on perl libs to reduce code duplication
- Detect nut UPS temp sensors

* Fri Jul 10 2015 Daniel B. <daniel@firewall-services.com> - 0.2.1-1
- Fix GlusterFS brick count on 3.7.x

* Fri Jul 10 2015 Daniel B. <daniel@firewall-services.com> - 0.2.0-1
- Migrate sensors config to an ini format
- Add a generator script which detects available sensors

* Tue Jul 7 2015 Daniel B. <daniel@firewall-services.com> - 0.1.27-1
- Support different sensors types

* Thu Jun 4 2015 Daniel B. <daniel@firewall-services.com> - 0.1.26-1
- Alert if a self heal is in progress on a glusterfs vol

* Thu Jun 4 2015 Daniel B. <daniel@firewall-services.com> - 0.1.25-1
- Fix gluster checks if info heal-failed is not supported

* Wed Apr 15 2015 Daniel B. <daniel@firewall-services.com> - 0.1.24-1
- Report a warning if a RAID array is resyncing

* Tue Feb 10 2015 Daniel B. <daniel@firewall-services.com> - 0.1.23-1
- Fix disco_filesystem to output valid JSON

* Thu Jan 8 2015 Daniel B. <daniel@firewall-services.com> - 0.1.22-1
- Fix check_qmail_sudo

* Mon Jan 5 2015 Daniel B. <daniel@firewall-services.com> - 0.1.21-1
- Add scripts to check qmail (requires qmqtool)

* Fri Nov 7 2014 Daniel B. <daniel@firewall-services.com> - 0.1.20-1
- discover LVM thin pools
- report LVM thin pools allocation

* Sun Sep 14 2014 Daniel B. <daniel@firewall-services.com> - 0.1.19-1
- Adapt squidclient commands to work with squid 3.1

* Wed Jul 16 2014 Daniel B. <daniel@firewall-services.com> - 0.1.18-1
- Add simple discovery and status check for GlusterFS

* Thu Jul 10 2014 Daniel B. <daniel@firewall-services.com> - 0.1.17-1
- Add discovery for MegaRAID controllers

* Wed Jul 9 2014 Daniel B. <daniel@firewall-services.com> - 0.1.16-1
- Add discovery script for mdadm based RAID devices

* Tue May 6 2014 Daniel B. <daniel@firewall-services.com> - 0.1.15-1
- Add a simple script to check nmb lookups

* Wed Feb 19 2014 Daniel B. <daniel@firewall-services.com> - 0.1.14-1
- remove scripts to discover and monitor certificates, they are too specific
  and are now in smeserver-zabbix-agent

* Tue Feb 18 2014 Daniel B. <daniel@firewall-services.com> - 0.1.13-1
- Move phpki conf to the correct location

* Tue Feb 18 2014 Daniel B. <daniel@firewall-services.com> - 0.1.12-1
- Add scripts to discover and monitor certificates (design to work with PHPki)

* Fri Nov 29 2013 Daniel B. <daniel@firewall-services.com> - 0.1.11-1
- Possibility to disable hosts monitoring in BackupPC by adding
  $Conf{ZabbixMonitoring} = 0 in the conf file

* Mon Oct 28 2013 Daniel B. <daniel@firewall-services.com> - 0.1.10-1
- Do not skip removable devices in disco_block_device

* Tue Oct 1 2013 Daniel B. <daniel@firewall-services.com> - 0.1.9-1
- Fix macros names in disco_raid_hp_sudo script

* Tue Oct 1 2013 Daniel B. <daniel@firewall-services.com> - 0.1.8-1
- Add simple scripts to monitor HP Smart Arrays

* Tue Apr 23 2013 Daniel B. <daniel@firewall-services.com> - 0.1.7-1
- Initialize an empty array in disco_backuppc_sudo
- Return more usefull macros in disco_backuppc_sudo
- Skip some blocks (loop, ram, dm) in disco_smart_sudo

* Mon Apr 22 2013 Daniel B. <daniel@firewall-services.com> - 0.1.6-1
- Fix permissions on sudoers fragment
- Use full path to smartctl binary

* Mon Apr 22 2013 Daniel B. <daniel@firewall-services.com> - 0.1.5-1
- Rewrite disco_smart_sudo in perl

* Thu Apr 18 2013 Daniel B. <daniel@firewall-services.com> - 0.1.4-1
- Possibility to pass a (base64 encoded) regex for backuppc hosts discovery
- Add nut ups scripts
- Fix lvm discovery on some systems

* Thu Apr 18 2013 Daniel B. <daniel@firewall-services.com> - 0.1.3-1
- Comment the manual net.if.discovery key

* Thu Apr 18 2013 Daniel B. <daniel@firewall-services.com> - 0.1.2-1
- Add network interface discovery scripts
- do not prepend /dev to block devices (not supported on older Zabbix agent)

* Wed Apr 17 2013 Daniel B. <daniel@firewall-services.com> - 0.1.1-1
- Fix a typo in smart.conf

* Wed Apr 17 2013 Daniel B. <daniel@firewall-services.com> - 0.1.0-1
- Initial release

