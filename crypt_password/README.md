# crypt_password

Perl script copied from the [Open WeBWorK Project](https://github.com/openwebwork), [bin/crypt_passwords_in_classlist.pl](https://raw.githubusercontent.com/openwebwork/webwork2/82052465024ba9ea27dba62cc604f92294501105/bin/crypt_passwords_in_classlist.pl).

Some information is in [Classlist Files](https://webwork.maa.org/wiki/Classlist_Files#Password_details) page on the wiki
and you can also see the [pull request](https://github.com/openwebwork/webwork2/pull/1461) in the WW code.

## Usage:

`crypt_passwords_in_classlist.pl <filename>`
where `<filename>` is a properly formatted WeBWorK classlist file with passwords in cleartext.

The output is the file `crypted_<filename>`, a properly formatted WeBWorK classlist with hashed passwords.