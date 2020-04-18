%define _unpackaged_files_terminate_build 0
# Relocate all the files to /opt/killer-commits
%global _prefix /opt/killer-commits
# Intresting _mandir is hardcoded to /usr/share/man and
# not %%_prefix/share/man - that's a bug.
%global _mandir %{_prefix}/share/man

Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl-static-openssl
Version: 7.69.1
Release: R1
License: MIT
Group: Applications/Internet
Source: http://curl.haxx.se/download/curl-%{version}.tar.gz
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/curl-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: redhat-rpm-config
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn-devel
BuildRequires: libssh2-devel >= 1.2

BuildRequires: openssl-devel
BuildRequires: openldap-devel
BuildRequires: openssh-clients
BuildRequires: openssh-server
BuildRequires: pkgconfig
BuildRequires: stunnel
BuildRequires: zlib-devel


%description
cURL static  package built with openssl instead of NSS.


%prep
%setup -q -n curl-%{version}

# Convert docs to UTF-8
for f in CHANGES README; do
	iconv -f iso-8859-1 -t utf8 < ${f} > ${f}.utf8
	mv -f ${f}.utf8 ${f}
done

%build
%configure --with-ssl --enable-ipv6 --without-ca-bundle --with-libidn  -with-zlib --with-secure-transport \
  	--enable-tls-srp --with-libssh2  --with-nghttp2 --with-ngtcp2  --with-nghttp3 \
	--with-quiche --with-gssapi --enable-ldaps  --disable-shared   --enable-static  --enable-manual   



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

%post 
[ -d %{_prefix}/curl_backup/  ] || mkdir %{_prefix}/curl_backup/ 

#curl_path=$(which curl)
#
#if [ -e $curl_path ]; then
#
#   mv -fi $curl_path %{_prefix}/curl_backup 
#	ln -s %{_bindir}/curl $curl_path
#
#	echo $curl_path  > %{_prefix}/curl_backup/link_path

if [  -e "/usr/bin/curl" ]; then
	mv -f /usr/bin/curl %{_prefix}/curl_backup 
	echo moving the current curl from /usr/bin/curl to backup location  %{_prefix}/curl_backup 
	ln -s %{_bindir}/curl /usr/bin/curl
	echo linking the curl-openssl with  /usr/bin/curl
	echo "/usr/bin/curl" > %{_prefix}/curl_backup/link_path
	echo saving the link location 

elif [  -e "/usr/local/bin/curl" ]; then
	mv -f /usr/local/bin/curl %{_prefix}/curl_backup 
	echo moving the current curl from  /usr/local/bin/curl to backup location  %{_prefix}/curl_backup 
	ln -s %{_bindir}/curl /usr/local/bin/curl
	echo linking the curl-openssl with  /usr/local/bin/curl
	echo "/usr/local/bin/curl" > %{_prefix}/curl_backup/link_path
	echo saving the link location 
else 
	echo curl not found in /usr/bin/curl and /usr/local/bin/curl
	ln -s %{_bindir}/curl /usr/local/bin/curl
	echo So linking the curl-openssl to the path  /usr/local/bin/curl
	echo "/usr/local/bin/curl" > %{_prefix}/curl_backup/link_path
	echo saving the link location , if there is any curl command , please save to backup location
fi
echo "Installed successfully :-) :-) :-)"


%postun
dest=$(<%{_prefix}/curl_backup/link_path) 
if [ -e %{_prefix}/curl_backup/curl ] 
then
	if [ -L $dest ] 
	then 
		unlink $dest
		echo Unlinking $dest
		cp %{_prefix}/curl_backup/curl $dest
		echo copying back the  actual curl from backup location %{_prefix}/curl_backup/curl to path  $dest
	else 
		echo Destination Link  path not found, i.e link path, orginal curl is safe in %{_prefix}/curl_backup/curl_path
		echo Move manually to the required path, cmd here =>  "  sudo cp  %{_prefix}/curl_backup/curl_path/curl  /to/you/destnation/path  " 
	fi 
else 
	if [ -L $dest ] 
	then 
		unlink $dest
		echo Unlinking $dest
	fi 
fi 
echo "UnInstalled successfully :-) :-) :-)" 






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