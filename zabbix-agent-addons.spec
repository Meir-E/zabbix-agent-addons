Summary: Scripts for Zabbix monitoring
Name: zabbix-agent-addons
Version: 0.1.21
Release: 1
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
Requires: perl(Linux::LVM)
Requires: perl(POSIX)
Requires: perl(MIME::Base64)
Requires: perl(File::Which)

AutoReqProv: no

%description
This package contains some usefull script to monitor
a Linux box with Zabbix. It provides helper scripts to
discover and monitor things like filesystems, block devices
LVM, RAID status, S.M.A.R.T. drives, BackupPC etc...

%prep
%setup -q

%build

%install

%{__rm} -rf $RPM_BUILD_ROOT

# Install zabbix scripts
%{__install} -d -m 750 $RPM_BUILD_ROOT%{_localstatedir}/lib/zabbix/bin
%{__install} -m 0755 zabbix_scripts/* $RPM_BUILD_ROOT%{_localstatedir}/lib/zabbix/bin
# Install Zabbix conf
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.conf.d/
%{__install} -m 0644 zabbix_conf/* $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.conf.d/
# Install sensors conf
%{__install} -m 0755 conf/sensors.conf $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/
# Install sudo conf
%{__install} -d 750 $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d
%{__install} -m 600 conf/sudo.conf $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d/zabbix_agent

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%preun

%post

%files
%defattr(-,root,root,-)
%doc README CHANGELOG.git
%dir %attr(0750,zabbix,zabbix) %{_localstatedir}/lib/zabbix/bin
%{_localstatedir}/lib/zabbix/bin/*
%config(noreplace) %attr(0640,root,zabbix) %{_sysconfdir}/zabbix/sensors.conf
%config(noreplace) %attr(0640,root,zabbix) %{_sysconfdir}/zabbix/zabbix_agentd.conf.d/*
%attr(0440,root,root) %{_sysconfdir}/sudoers.d/*

%changelog
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

