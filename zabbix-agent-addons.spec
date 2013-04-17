Summary: Scripts for Zabbix monitoring
Name: zabbix-agent-addons
Version: 0.1.1
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
%attr(0600,root,root) %{_sysconfdir}/sudoers.d/*

%changelog
* Wed Apr 17 2013 Daniel B. <daniel@firewall-services.com> - 0.1.1-1
- Fix a typo in smart.conf

* Wed Apr 17 2013 Daniel B. <daniel@firewall-services.com> - 0.1.0-1
- Initial release

