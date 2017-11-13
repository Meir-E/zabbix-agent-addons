%if 0%{?rhel} && 0%{?rhel} < 7
%global _without_selinux 1
%endif

Summary: Scripts for Zabbix monitoring
Name: zabbix-agent-addons
Version: 0.2.20
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
Requires: perl(Linux::LVM)
Requires: perl(POSIX)
Requires: perl(MIME::Base64)
Requires: perl(File::Which)
Requires: perl(Config::Simple)
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
%doc README CHANGELOG.git
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

