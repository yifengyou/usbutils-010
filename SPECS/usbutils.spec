Name:    usbutils
Summary: Linux USB utilities
Version: 010
Release: 3%{?dist}
URL:     http://www.linux-usb.org/
License: GPLv2+

Source0: https://www.kernel.org/pub/linux/utils/usb/usbutils/%{name}-%{version}.tar.xz
Source1: GPL-2.0.txt
Source2: GPL-3.0.txt

#Patch1: 0001-SPDX-bill-of-material-is-supposed-to-be-project_name.patch
#Patch2: 0002-Makefile.am-add-files-with-licenses-to-archive.patch
Patch3: 0003-usbutils.spdx-rerun-report-it-is-properly-sorted.patch
Patch4: 0004-lsusb.py-fix-up-Python-3-conversion.patch
Patch5: 0005-lsusb-Split-out-routine-that-fetches-value-for-given.patch
Patch6: 0006-lsusb-Split-out-field-name-rendering.patch
Patch7: 0007-lsusb-Add-support-for-descriptor-extensions.patch
Patch8: 0008-lsusb-Add-support-for-audio-processing-unit-type-spe.patch
Patch9: 0009-desc-dump.c-fix-compiler-warning-about-unused-variab.patch

%global num_patches %{lua: c=0; for i,p in ipairs(patches) do c=c+1; end; print(c);}

BuildRequires: libusbx-devel
BuildRequires: systemd-devel
BuildRequires: python3-devel
BuildRequires: git
Requires: hwdata

%description
This package contains utilities for inspecting devices connected to a
USB bus.

%prep
%setup -q

pathfix.py -i %{__python3} -pn lsusb.py.in

%if %{num_patches}
git init
git config user.email "usbutils@redhat.com"
git config user.name "usbutils"
git add .
git commit -a -q -m "%{version} baseline."

# Apply all the patches.
git am --exclude=project_name.spdx --exclude=bom.spdx --exclude=usbutils.spdx %{patches}
%endif

%build
%configure --sbindir=%{_sbindir} --datadir=%{_datadir}/hwdata --disable-usbids
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -rf %{buildroot}/%{_libdir}/pkgconfig/usbutils.pc

#FIXME: remove with usbutils-011
mkdir -p %{buildroot}%{_prefix}/share/licenses/usbutils/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/share/licenses/usbutils/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/share/licenses/usbutils/

%files
%{!?_licensedir:%global license %%doc}
%license GPL-2.0.txt GPL-3.0.txt
%doc NEWS
%{_mandir}/*/*
%{_bindir}/*

%changelog
* Wed Aug 01 2018 Charalampos Stratakis <cstratak@redhat.com> - 010-3
- Fix python shebangs

* Fri Jun 08 2018 Lukas Nykryn <lnykryn@redhat.com> - 010-2
- add upstream fixes

* Wed May 16 2018 Lukas Nykryn <lnykryn@redhat.com> - 010-1
- New 010 release

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec  4 2017 Peter Robinson <pbrobinson@fedoraproject.org> 009-1
- New 009 release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 008-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 008-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 008-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 29 2016 Peter Robinson <pbrobinson@fedoraproject.org> 008-6
- Don't ship usbutils pkgconfig file

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 008-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jul 19 2015 Peter Robinson <pbrobinson@fedoraproject.org> 008-4
- Fix FTBFS, cleanup and modernise spec, use %%license

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 008-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Oct 22 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 008-1
- new release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 007-1
- new upstream release

* Tue Feb 26 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 006-4
- lsusb-t: make sure that interfaces are added to lists only once (#914929)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Lukáš Nykrýn <lnykryn@redhat.com> - 006-1
- new upstream release

* Thu Apr 19 2012 Lukas Nykryn <lnykryn@redhat.com> 005-1
- new upstream release

* Thu Apr 19 2012 Lukas Nykryn <lnykryn@redhat.com> 004-4
- Ignore missing driver symlink (#808934)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
