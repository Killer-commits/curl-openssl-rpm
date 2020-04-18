# Relocate all the files to /opt/killer-commits
%global _prefix /opt/killer-commits
# Intresting _mandir is hardcoded to /usr/share/man and
# not %%_prefix/share/man - that's a bug.
%global _mandir %{_prefix}/share/man

Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl-openssl
Version: 7.69.1
Release: R2
License: MIT
Group: Applications/Internet
Source: http://curl.haxx.se/download/curl-%{version}.tar.gz
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/curl-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake
BuildRequires: redhat-rpm-config
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn-devel
#BuildRequires: libssh2-devel >= 1.2
#BuildRequires: nss-devel
BuildRequires: openssl-devel
BuildRequires: openldap-devel
#BuildRequires: openssh-clients
#BuildRequires: openssh-server
BuildRequires: pkgconfig
BuildRequires: stunnel
Requires : libssh2 >= 1.8.0
BuildRequires: zlib-devel
Requires: libcurl-openssl = %{version}-%{release}

# We do not want curl-openssl to provide or require the 
#.so and similar  files that the real curl provides so we must 
# filter them out.
%filter_provides_in %{_libdir}/.*\.so.*$ 
%filter_from_provides /pkgconfig(libcurl)/d
%filter_from_requires /libcurl\.so\..*/d
%filter_setup

%description
cURL package built with openssl and  NSS.

%package -n libcurl-openssl
Summary: A library for getting files from web servers
Group: Development/Libraries

# libssh2 ABI has been changed since libssh2-1.0
# this forces update of libssh2 before update of libcurl
#Requires: libssh2 >= 1.2

%description -n libcurl-openssl
cURL package built with openssl instead of NSS.

%package -n libcurl-openssl-devel
Summary: Files needed for building applications with libcurl-openssl
Group: Development/Libraries
Requires: automake
Requires: libcurl-openssl = %{version}-%{release}
Requires: libidn-devel
Requires: pkgconfig

%description -n libcurl-openssl-devel
The libcurl-openssl-devel package includes files needed for
developing applications which can use cURL's capabilities internally.

%prep
%setup -q -n curl-%{version}

# Convert docs to UTF-8
for f in CHANGES README; do
	iconv -f iso-8859-1 -t utf8 < ${f} > ${f}.utf8
	mv -f ${f}.utf8 ${f}
done

%build
%configure --with-ssl --disable-static --enable-hidden-symbols --with-gssapi --with-libidn \
			--enable-ipv6 --enable-ldaps --enable-manual --enable-threaded-resolver \
			--with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt --with-libssh2 

sed -i -e 's,-L/usr/lib ,,g;s,-L/usr/lib64 ,,g;s,-L/usr/lib$,,g;s,-L/usr/lib64$,,g' \
	Makefile libcurl.pc
# Remove bogus rpath
sed -i \
	-e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
	-e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p" install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la

install -d $RPM_BUILD_ROOT%{_datadir}/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

# We don't update the central cache but do create the symlinks.
# %post -n libcurl-openssl
# /sbin/ldconfig -N %{_libdir}

# %postun -n libcurl-openssl 
# /sbin/ldconfig -N %{_libdir}


%post 
[ -d %{_prefix}/curlbackup ] || mkdir %{_prefix}/curlbackup
[ -d %{_prefix}/curlbackup/lib64/  ] || mkdir %{_prefix}/curlbackup/lib64
[ -d %{_prefix}/curlbackup/bin/  ] || mkdir %{_prefix}/curlbackup/bin
echo  "---------------------------"
mv -f /usr/lib64/libcurl.s*    %{_prefix}/curlbackup/lib64/
echo "/usr/lib64/libcurl.s* files moved safely to " %{_prefix}/curlbackup/lib64/
echo $(ls -l %{_prefix}/curlbackup/lib64/)
echo  "---------------------------"
mv -f  /usr/bin/curl    %{_prefix}/curlbackup/bin/
echo "/usr/bin/curl file is moved safely to " %{_prefix}/curlbackup/bin/
echo $(ls -l %{_prefix}/curlbackup/bin/)

echo  "---------------------------"
find %{_libdir} -name 'libcurl.s*' | while read libcurlfile; do
    filename=$(basename $libcurlfile)
    ln -s $libcurlfile /usr/lib64/$filename
    echo Linked $libcurlfile to /usr/lib64/$filename
done
echo  "---------------------------"
ln -s %{_bindir}/curl /usr/bin/curl
echo Linked {_bindir}/curl to /usr/bin/curl
echo  "---------------------------"
echo "Curl-openssl installer assumed curl binary in /usr/bin/curl and Libs in /usr/lib64, if not please take care"
echo  "Installed successfully :-) :-) :-) "
echo  "---------------------------"


%postun
echo  "---------------------------"
find %{_libdir} -name 'libcurl.s*' | while read libcurlfile; do
	filename=$(basename $libcurlfile)
 
	if [ -L /usr/lib64/$filename ]
	then
    	unlink  /usr/lib64/$filename
    	echo Unlinked  /usr/lib64/$filename
	fi
done
echo  "---------------------------"
echo Files with name libcurl.s* in  /usr/lib64 before 
echo $(ls /usr/lib64/ | grep libcurl.s* )
echo  
echo coping the lib files $(ls %{_prefix}/curlbackup/lib64/ | grep libcurl.s* ) to /usr/lib64
cp -f  %{_prefix}/curlbackup/lib64/libcurl.s* /usr/lib64/
echo copied successfully the lib files 
echo $(ls /usr/lib64/ | grep libcurl.s* )
echo  "---------------------------"
if [ -L "/usr/bin/curl" ]
then
	unlink /usr/bin/curl
	echo Unlinked /usr/bin/curl
fi
cp -f %{_prefix}/curlbackup/bin/curl /usr/bin/
echo "Copied successfully curl file from  %{_prefix}/curlbackup/bin/curl to /usr/bin/ " 
echo "ls /usr/bin | grep curl"
echo $(ls /usr/bin | grep curl)
echo  "---------------------------"
echo "Uninstalled successfully :-) :-) :-) "
echo  "---------------------------"


%files
%defattr(-,root,root,-)
%doc CHANGES README* COPYING
%doc docs/BUGS docs/FAQ docs/FEATURES
%doc docs/RESOURCES
%doc docs/TheArtOfHttpScripting docs/TODO
%dir %{_bindir}
%{_bindir}/curl
%dir %{_mandir}
%dir %{_mandir}/man1
%{_mandir}/man1/curl.1*

%files -n libcurl-openssl
%defattr(-,root,root,-)
%dir %{_prefix}
%dir %{_libdir}
%{_libdir}/libcurl.so.*

%files -n libcurl-openssl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example
%doc docs/libcurl/ABI
%dir %{_bindir}
%dir %{_includedir}
%dir %{_libdir}/pkgconfig
%dir %{_mandir}
%dir %{_mandir}/man1
%dir %{_mandir}/man3
%dir %{_datadir}
%dir %{_datadir}/aclocal
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4
