Title: Using PKCS#11 on GNU/Linux
Date: 2016-08-07 20:17
Tags: pkcs11, debian
Category: hacks
Slug: pkcs11
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag

PKCS#11 is a standard API to interface with HSMs, Smart Cards, or other types
of random hardware backed crypto. On my travel laptop, I use a few Yubikeys in
PKCS#11 mode using OpenSC to handle system login. `libpam-pkcs11` is a pretty
easy to use module that will let you log into your system locally using a
PKCS#11 token locally.

One of the least documented things, though, was how to use an OpenSC PKCS#11
token in Chrome. First, close all web browsers you have open.

```
sudo apt-get install libnss3-tools

certutil -U -d sql:$HOME/.pki/nssdb
modutil -add "OpenSC" -libfile /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so -dbdir sql:$HOME/.pki/nssdb
modutil -list "OpenSC" -dbdir sql:$HOME/.pki/nssdb 
modutil -enable "OpenSC" -dbdir sql:$HOME/.pki/nssdb
```

Now, we'll have the PKCS#11 module ready for `nss` to use, so let's double
check that the tokens are registered:

```
certutil -U -d sql:$HOME/.pki/nssdb
certutil -L -h "OpenSC" -d sql:$HOME/.pki/nssdb
```

If this winds up causing issues, you can remove it using the following
command:

```
modutil -delete "OpenSC" -dbdir sql:$HOME/.pki/nssdb
```
