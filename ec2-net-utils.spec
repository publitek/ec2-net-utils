Name:      ec2-net-utils
Summary:   A set of tools for automatic discovery and configuration of network interfaces in AWS cloud
Version:   1.0.0
Release:   1
License:   Apache License 2.0
Group:     System Tools
Packager:  Ben Youngblut <by@fotosearch.com>
Source:    %{name}-%{version}.tar.gz
BuildArch: noarch
Requires:  initscripts
Requires:  bash >= 4
Requires:  curl
Requires:  iproute
BuildRequires: systemd-units

%description
A set of tools for automatic discovery and configuration of network interfaces in AWS cloud.

%prep
%setup

%build

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}/sbin
%{__mkdir_p} %{buildroot}%{_sysconfdir}/udev/rules.d/
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
%{__mkdir_p} %{buildroot}%{_sysconfdir}/dhcp/dhclient.d/
%{__mkdir_p} %{buildroot}%{_mandir}/man8/
%{__install} -m755 ec2ifup %{buildroot}/sbin/
%{__install} -m755 ec2ifdown %{buildroot}/sbin/
%{__install} -m755 ec2ifscan %{buildroot}/sbin/
%{__install} -m755 ec2ifsync %{buildroot}/sbin/
%{__install} -m644 53-ec2-network-interfaces.rules %{buildroot}%{_sysconfdir}/udev/rules.d/
%{__install} -m644 ec2net-functions %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
%{__install} -m755 ec2net.hotplug %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
%{__install} -m755 ec2dhcp.sh %{buildroot}%{_sysconfdir}/dhcp/dhclient.d/
%{__install} -m644 ec2ifup.8 %{buildroot}%{_mandir}/man8/ec2ifup.8
ln -s ./ec2ifup.8.gz %{buildroot}%{_mandir}/man8/ec2ifdown.8.gz
%{__install} -m644 ec2ifscan.8 %{buildroot}%{_mandir}/man8/ec2ifscan.8
%{__install} -d -m 0775 %{buildroot}%{_unitdir}
%{__install} -m 0644 elastic-network-interfaces.service %{buildroot}%{_unitdir}
%{__install} -m 0644 ec2-ifup@.service %{buildroot}%{_unitdir}
%{__install} -m644 -D ixgbevf.conf %{buildroot}/etc/modprobe.d/ixgbevf.conf
%{__install} -m755 -D acpiphp.modules %{buildroot}/etc/sysconfig/modules/acpiphp.modules

%clean
rm -rf %{buildroot}

%files
/sbin/ec2ifup
/sbin/ec2ifdown
/sbin/ec2ifscan
/sbin/ec2ifsync
%{_sysconfdir}/udev/rules.d/53-ec2-network-interfaces.rules
%{_sysconfdir}/modprobe.d/ixgbevf.conf
%{_sysconfdir}/sysconfig/modules/acpiphp.modules
%{_sysconfdir}/sysconfig/network-scripts/ec2net-functions
%{_sysconfdir}/sysconfig/network-scripts/ec2net.hotplug
%{_sysconfdir}/dhcp/dhclient.d/ec2dhcp.sh
%{_mandir}/man8/ec2ifup.8.gz
%{_mandir}/man8/ec2ifdown.8.gz
%{_mandir}/man8/ec2ifscan.8.gz
%{_unitdir}/elastic-network-interfaces.service
%{_unitdir}/ec2-ifup@.service

%post
%systemd_post elastic-network-interfaces.service
%systemd_post ec2-ifup@.service

%preun
%systemd_preun elastic-network-interfaces.service
%systemd_preun ec2-ifup@.service

%postun
%systemd_postun elastic-network-interfaces.service
%systemd_postun ec2-ifup@.service

%changelog
* Wed Mar 29 2017 Ben Youngblut <by@fotosearch.com>
- Made into RPM for CentOS 7

* Tue Sep 24 2013 Andrew Jorgensen <ajorgens@amazon.com>
- Add hotplug script and module config

* Mon Aug 26 2013 Ben Cressey <bcressey@amazon.com>
- Configure interfaces attached at launch time

* Wed Mar 13 2013 Andrew Jorgensen <ajorgens@amazon.com>
- Use -q to avoid using a user's .curlrc

* Sun Sep 16 2012 Ben Cressey <bcressey@amazon.com>
- Add documentation for ec2ifup and ec2ifdown

* Thu Sep 13 2012 Ben Cressey <bcressey@amazon.com>
- Optimize metadata queries for elastic interfaces

* Tue Sep 11 2012 Ben Cressey <bcressey@amazon.com>
- Adjust route table usage for elastic interfaces
- Update headers to reflect Apache 2.0 license

* Wed Sep 5 2012 Ben Cressey <bcressey@amazon.com>
- Configure elastic network interfaces via DHCP

* Wed Aug 29 2012 Andrew Jorgensen <ajorgens@amazon.com>
- Add dependency on curl for ec2-metadata
- Update ec2-metadata to 0.1.1 bugfix release

* Mon Aug 13 2012 Ben Cressey <bcressey@amazon.com>
- Add rules and scripts for MultiIP / MultiVIF support

* Mon Jul 30 2012 Ethan Faust <efaust@amazon.com>
- Added udev rules to automatically bring up vCPUs when they're added.

* Mon Aug 1 2011 Nathan Blackham <blackham@amazon.com>
- adding BuildRoot directive to specfile.

* Wed Sep 22 2010 Nathan Blackham <blackham@amazon.com>
- move to ec2-utils
- add udev code for symlinking xvd* devices to sd*
- fixing typo in spec file
- adding udev symlinks for xvd* devices

* Tue Sep 07 2010 Nathan Blackham <blackham@amazon.com>
- initial packaging of script as an rpm
- moving rpm to noarch
- adding Group line in specfile
- initial packaging of ec2-metadata
- setup complete for package ec2-metadata
