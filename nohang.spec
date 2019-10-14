%global commit      2a3209ca72616a6a8f59711ff7fde7a6662ff3c7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date        20191005

Name:           nohang
Version:        0.1
Release:        15.%{date}git%{shortcommit}%{?dist}
Summary:        Highly configurable OOM prevention daemon

License:        MIT
URL:            https://github.com/hakavlad/nohang
Source0:        %{url}/archive/%{commit}/%{name}-%{version}.%{date}git%{shortcommit}.tar.gz
BuildArch:      noarch

%if 0%{?el7}
BuildRequires:  systemd
%else
BuildRequires:  systemd-rpm-macros
%endif
Requires:       logrotate
%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends:     %{name}-desktop
%endif
%{?systemd_requires}

%description
Nohang is a highly configurable daemon for Linux which is able to correctly
prevent out of memory (OOM) and keep system responsiveness in low
memory conditions.

To enable and start:

  systemctl enable --now %{name}


%package        desktop
Summary:        Desktop version of %{name}
BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}
Requires:       libnotify

%description    desktop
Desktop version of %{name}.


%prep
%autosetup -p1 -n %{name}-%{commit}


%build
%make_build


%install
%make_install BINDIR=%{_bindir} CONFDIR=%{_sysconfdir} SYSTEMDUNITDIR=%{_unitdir}
# E: zero-length /etc/nohang/version
# https://github.com/hakavlad/nohang/issues/52
echo "v%{version}-%{shortcommit}" > %{buildroot}%{_sysconfdir}/%{name}/version


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%post desktop
install -p -m 0644 %{_sysconfdir}/%{name}/%{name}-desktop.conf %{_sysconfdir}/%{name}/%{name}.conf


%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/%{name}
%{_bindir}/oom-sort
%{_bindir}/psi-monitor
%{_bindir}/psi-top
%{_mandir}/man1/*.*
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_sysconfdir}/%{name}/%{name}.conf.default
%{_sysconfdir}/%{name}/version
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}

%files desktop
%{_sysconfdir}/%{name}/%{name}-desktop.conf


%changelog
* Mon Oct 14 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-15.20191005git2a3209c
- Update to latest git snapshot

* Thu Sep 19 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-14.20190919git286ed84
- Update to latest git snapshot

* Tue Sep 10 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-10.20190910gite442e41
- Update to latest git snapshot
- Add 'desktop' package

* Thu Sep 05 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-8.20190905git6db1833
- Update to latest git snapshot

* Sun Sep 01 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-7.20190901git4c1b5ee
- Update to latest git snapshot

* Sat Aug 31 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-5.20190831gitf3baa58
- Initial package

