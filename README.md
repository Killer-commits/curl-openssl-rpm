# cURL OpenSSL RPMs

The CentOS has cURL with NSS , This version of cURL has openssl, thats all.

### Why this package was created?

In ```CentOS Linux 7 (Core)``` with  ```curl 7.29.0 (x86_64-redhat-linux-gnu) libcurl/7.29.0 NSS/3.44 zlib/1.2.7 libidn/1.28 libssh2/1.8.0
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp scp sftp smtp smtps telnet tftp
Features: AsynchDNS GSS-Negotiate IDN IPv6 Largefile NTLM NTLM_WB SSL libz unix-sockets```


the following error happend during connection 

```
* Doing the SSL/TLS handshake on the data stream
* skipping SSL peer certificate verification
* NSS error -5938 (PR_END_OF_FILE_ERROR)
* Encountered end of file
* Failure sending ABOR command: SSL connect error
* Closing connection 0
curl: (35) Encountered end of file
```

To resolve this issue with my limited knowledge, cURL with openssl was build 

# Download

## curl-static-openssl
**[curl-static-openssl Download here](https://github.com/Killer-commits/curl-openssl-rpm/releases/tag/R1) **

This version doesnot need any shared library (.so files , shared object files) , just a single binary which will help to overcome the issue. Most of the case

#### Installing curl-static-openssl

- ```sudo rpm -i curl-static-openssl-7.69.1-R1.x86_64.rpm```

    During in installing process, the following things happens
    - The original cURL at ```/usr/bin/curl``` is moved to ```/opts/killer-commits/curl_backup/```

-  ```curl -V``` verify by checking version 

#### Uninstalling curl-static-openssl

- ```sudo rpm -i curl-static-openssl-7.69.1-R1.x86_64.rpm```

    During in uninstalling process, the following things happens
    - The original cURL at  ```/opts/killer-commits/curl_backup/curl```  is moved back to ```/usr/bin/curl```

-  ```curl -V``` verify by checking version 

![Install and Uninstalaling curl-static-openssl-rpm Demo Image](../../blob/master/screenshot/curl-staic-openssl-demo.JPG)


## curl-openssl

**[### curl-openssl Download  here](https://github.com/Killer-commits/curl-openssl-rpm/releases/tag/R2)**
This cURL is build with enable share , which means the shared object are required to run ```libcurl-openssl```.

Addiditonally a  ```libcurl-openssl-devel``` file will be there  which is used to build another application from libcurl , for exapmle :  ```pycurl with openssl  for python``` or for ```php``` you can use this one.


### Installing curl-openssl
Please follow the order for installation as given below 

- ```sudo rpm -i libcurl-openssl-7.69.1-R2.x86_64.rpm```

- ```sudo rpm -i libcurl-openssl-devel-7.69.1-R2.x86_64.rpm ``` (**libcurl-openssl-devel is optional**, for example if you need  curl-config or  then install it . ```libcurl-devel``` requires  ```libidn-devel``` , get it by ```sudo yum install libidn-devel```)

- ```sudo rpm -i curl-openssl-7.69.1-R2.x86_64.rpm```

    During in installing last file , the following things happens
    - The original cURL at ```/usr/bin/curl``` is moved to ```/opts/killer-commits/curlbackup/bin/```
    - The original libcurl files ```/usr/lib64/libcurl.s*``` are moved ```/opts/killer-commits/curlbackup/lib64/```. Only moving libcurl.s* files form lib64

- ```curl -V``` verify by checking version 

![Install curl-openssl-rpm Demo Image](../../blob/master/screenshot/curl-openssl-install-demo.JPG)

### Uninstalling curl-openssl

- ```sudo rpm -e curl-openssl-7.69.1-R2.x86_64```
    
    During in uninstalling last file , the following things happens
    - The original cURL at ```/opts/killer-commits/curlbackup/bin/curl``` is moved back o ```/usr/bin/```
    - The original libcurl files from ```/opts/killer-commits/curlbackup/lib64/libcurl.s*```  are moved back ```/usr/lib64/```.

- ```sudo rpm -e libcurl-openssl-devel-7.69.1-R2.x86_64```

- ```sudo rpm -e libcurl-openssl-7.69.1-R2.x86_64```

- ```curl -V``` verify by checking version 

![Uninstall curl-openssl-rpm Demo Image](../../blob/master/screenshot/curl-openssl-uninstall-demo.JPG)

If you want to build please follow the below instruction 

# Build Instructions

```
sudo yum groupinstall "Development Tools"
sudo yum install yum-utils
git clone https://github.com/killer-commits/curl-openssl.git ~/rpmbuild
wget -P ~/rpmbuild/SOURCES/https://curl.haxx.se/download/curl-7.69.1.tar.gz
cd ~/rpmbuild/SPECS
sudo yum-builddep curl.spec
rpmbuild -bb curl.spec
sudo rpm -i ~/rpmbuild/RPMS/x86_64/*.rpm
```

# License 
# :-) 
