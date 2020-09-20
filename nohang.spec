%global commit 2500c6cef7d1a10cddb47b8976335242af77c7ea
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200809

Name: nohang
Version: 0.1
Release: 32.%{date}git%{shortcommit}%{?dist}
Summary: Sophisticated low memory handler for Linux
BuildArch: noarch

License: MIT
URL: https://github.com/hakavlad/nohang
Source0: %{url}/archive/%{commit}/%{name}-%{version}.%{date}git%{shortcommit}.tar.gz

BuildRequires: gettext
%if 0%{?rhel} >= 7
BuildRequires: systemd
%else
BuildRequires: systemd-rpm-macros
%endif

Requires: logrotate

%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends: %{name}-desktop
%endif

%{?systemd_requires}

%description
Nohang is a highly configurable daemon for Linux which is able to correctly
prevent out of memory (OOM) and keep system responsiveness in low memory
conditions.

To enable and start:

  systemctl enable --now %{name}


%package desktop
Summary: Desktop version of %{name}
BuildArch: noarch

Requires: %{name} = %{version}-%{release}
Requires: libnotify

%description desktop
Desktop version of %{name}.


%prep
%autosetup -n %{name}-%{commit} -p1


%build
%make_build


%install
%make_install \
    BINDIR=%{_bindir} \
    MANDIR=%{_mandir}/man1 \
    PREFIX=%{_prefix} \
    SYSCONFDIR=%{_sysconfdir} \
    SYSTEMDUNITDIR=%{_unitdir}

# E: zero-length /etc/nohang/version
# * https://github.com/hakavlad/nohang/issues/52
echo "v%{version}-%{shortcommit}" > %{buildroot}%{_datadir}/%{name}/version


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

# Desktop
%post desktop
%systemd_post %{name}-desktop.service

%preun desktop
%systemd_preun %{name}-desktop.service

%postun desktop
%systemd_postun_with_restart %{name}-desktop.service


%files
%license LICENSE
%{_sbindir}/%{name}
%{_bindir}/oom-sort
%{_bindir}/psi-top
%{_bindir}/psi2log
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/%{name}/%{name}.conf
%{_datadir}/%{name}/version
%{_docdir}/%{name}/*.md
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}/

%files desktop
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-desktop.conf
%{_datadir}/%{name}/%{name}-desktop.conf
%{_unitdir}/%{name}-desktop.service


%changelog
* Mon Aug 10 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-32.20200809git2500c6c
- Update to latest git snapshot

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-31.20200612git271c04d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 12 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-30.20200612git271c04d
- Update to latest git snapshot

* Wed May 06 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-29.20200506git4cf9810
- Update to latest git snapshot

* Mon May 04 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-28.20200504gita794396
- Update to latest git snapshot

* Sun Apr 26 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-27.20200426git45b15aa
- Update to latest git snapshot
- Update summary, sync with upstream

* Fri Apr 03 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-26.20200403git18f90d7
- Update to latest git snapshot

* Mon Mar 23 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-25.20200323gitdaca5cc
- Update to latest git snapshot

* Tue Mar 17 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-24.20200317gitc70b824
- Update to latest git snapshot

* Fri Feb 28 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-23.20200228git2928709
- Update to latest git snapshot

* Fri Feb 21 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-22.20200221git8cc7c63
- Update to latest git snapshot

* Tue Feb 18 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-21.20200218git4925df0
- Update to latest git snapshot

* Sun Feb 02 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-20.20200202gite6eace7
- Update to latest git snapshot

* Fri Jan 31 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-19.20200131git6fb0324
- Update to latest git snapshot

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-18.20191203git6389a06
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 04 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-17.20191203git6389a06
- Update to latest git snapshot

* Sun Nov 17 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-16.20191117gitaef8af6
- Update to latest git snapshot

* Mon Oct 14 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-15.20191005git2a3209c
- Update to latest git snapshot

* Sat Sep 21 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.1-15.20190919git286ed84
- Fix BR: systemd required for EPEL8

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
