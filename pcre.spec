Name: pcre
Version: 7.8
Release: 3.1%{?dist}
Summary: Perl-compatible regular expression library
URL: http://www.pcre.org/
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.bz2
Patch0: pcre-7.3-multilib.patch
License: BSD
Group: System Environment/Libraries
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary: Static library for %{name}
Group: Development/Libraries

%description static
Library for static linking for %{name}.

%prep
%setup -q
%patch0 -p1 -b .multilib

%build
%configure --enable-utf8 --enable-unicode-properties

# One contributor's name is non-utf8
iconv -f latin1 -t utf8 ChangeLog >ChangeLog.utf8
touch --reference ChangeLog ChangeLog.utf8
mv ChangeLog.utf8 ChangeLog

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libpcre.so.* $RPM_BUILD_ROOT/%{_lib}/
pushd $RPM_BUILD_ROOT%{_libdir}
ln -fs ../../%{_lib}/libpcre.so.0 libpcre.so
popd

# get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/%{_lib}/*.so.*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_bindir}/pcregrep
%{_bindir}/pcretest
%doc AUTHORS COPYING LICENCE NEWS README ChangeLog

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man3/*
%{_bindir}/pcre-config
%doc doc/*.txt doc/html
%doc HACKING

%files static
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 7.8-3.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 1 2008 Lubomir Rintel <lkundrak@v3.sk> - 7.8-1
- Update to 7.8, drop upstreamed patches
- Fix destination of documentation (#427763)
- Use buildroot macro consistently
- Separate the static library, as per current Guidelines
- Satisfy rpmlint

* Fri Jul  4 2008 Tomas Hoger <thoger@redhat.com> - 7.3-4
- Apply Tavis Ormandy's patch for CVE-2008-2371.

* Tue Feb 12 2008 Tomas Hoger <thoger@redhat.com> - 7.3-3
- Backport patch from upstream pcre 7.6 to address buffer overflow
  caused by "a character class containing a very large number of
  characters with codepoints greater than 255 (in UTF-8 mode)"
  CVE-2008-0674, #431660
- Try re-enabling make check again.

* Fri Nov 16 2007 Stepan Kasal <skasal@redhat.com> - 7.3-2
- Remove obsolete ``reqs''
- add dist tag
- update BuildRoot

* Mon Sep 17 2007 Than Ngo <than@redhat.com> - 7.3-1
- bz292501, update to 7.3

* Mon Jan 22 2007 Than Ngo <than@redhat.com> - 7.0-1
- 7.0

* Mon Nov 27 2006 Than Ngo <than@redhat.com> - 6.7-1
- update to 6.7
- fix #217303, enable-unicode-properties
- sane stack limit

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.6-1.1
- rebuild

* Tue May 09 2006 Than Ngo <than@redhat.com> 6.6-1
- update to 6.6
- fix multilib problem

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Aug 24 2005 Than Ngo <than@redhat.com> 6.3-1
- update to 6.3

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 5.0-4
- rebuild

* Fri Feb 11 2005 Joe Orton <jorton@redhat.com> 5.0-3
- don't print $libdir in 'pcre-config --libs' output

* Thu Nov 18 2004 Joe Orton <jorton@redhat.com> 5.0-2
- include LICENCE, AUTHORS in docdir
- run make check
- move %%configure to %%build

* Thu Nov 18 2004 Than Ngo <than@redhat.com> 5.0-1
- update to 5.0
- change License: BSD
- fix header location #64248

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 23 2004 Than Ngo <than@redhat.com> 4.5-2
- add the correct pcre license, #118781

* Fri Mar 12 2004 Than Ngo <than@redhat.com> 4.5-1
- update to 4.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 4.4-1
- 4.4

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  7 2003 Than Ngo <than@redhat.com> 4.2-1
- update to 4.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Than Ngo <than@redhat.com> 3.9-9
- build with utf8, bug #81504

* Fri Nov 22 2002 Elliot Lee <sopwith@redhat.com> 3.9-8
- Really remove .la files

* Fri Oct 11 2002 Than Ngo <than@redhat.com> 3.9-7
- remove .la

* Thu Oct 10 2002 Than Ngo <than@redhat.com> 3.9-7
- Typo bug

* Wed Oct  9 2002 Than Ngo <than@redhat.com> 3.9-6
- Added missing so symlink

* Thu Sep 19 2002 Than Ngo <than@redhat.com> 3.9-5.1
- Fixed to build s390/s390x/x86_64

* Wed Jun 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-5
- Fix #65009

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-2
- rebuild

* Fri Jan 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-1
- Update to 3.9

* Wed Nov 14 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.7-1
- Update to 3.7

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.4-2
- Move libpcre to /lib, grep uses it these days (#41104)

* Wed Apr 18 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Move this to a separate package, used to be in kdesupport, but it's
  generally useful...
