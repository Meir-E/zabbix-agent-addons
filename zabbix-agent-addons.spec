Summary: Scripts for Zabbix monitoring
Name: zabbix-agent-addons
Version: 0.0.1
Release: 1.beta0
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

License: GPL
Group: Virtualization
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Requires: zabbix-agent

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
%{__install} -d -m 750 -o zabbix -g zabbix $RPM_BUILD_ROOT%{_localstatedir}/lib/zabbix/bin
%{__install} -m 0755 zabbix_scripts/* $RPM_BUILD_ROOT%{_localstatedir}/lib/zabbix/bin
# Install Zabbix conf
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.conf.d/
%{__install} -m 0755 zabbix_conf/* $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.conf.d/
# Install sudo conf
%{__install} -d 750 $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d
%{__install} conf/suydo.conf $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%preun

%post

%files
%defattr(-,root,root,-)
%doc README CHANGELOG.git
%{_localstatedir}/lib/zabbix/bin
%{_sysconfdir}/zabbix/zabbix_agentd.conf.d/
%{_sysconfdir}/sudoers.d

%changelog
* Mon Apr 15 2013 Daniel B. <daniel@firewall-services.com> - 0.0.1-1
- Initial release

