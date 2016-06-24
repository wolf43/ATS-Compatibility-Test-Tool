# ATS Compatability Test Tool(ACTT)

### Introduction
Advanced transport security(ATS) is a set of requirements set by Apple(the software company, not fruit) for TLS configuration of servers used by iOS apps

###
Requirements
Here is the extract from Apple's documentation about the requirements:  
"""  

With ATS fully enabled, your app’s HTTP connections must use HTTPS and must satisfy the following security requirements:  
The server certificate must meet at least one of the following trust requirements:  
* Issued by a certificate authority (CA) whose root certificate is incorporated into the operating system
* Issued by a trusted root CA and installed by the user or a system administrator  
The negotiated Transport Layer Security version must be TLS 1.2  
The negotiated TLS connection cipher suite must support forward secrecy (FS) and be one of the following:  
TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384  
TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256  
TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384  
TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA  
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256  
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA  
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  
TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384  
TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256  
TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA  
The leaf server certificate must be signed with one of the following types of keys:  
* Rivest-Shamir-Adleman (RSA) key with a length of at least 2048 bits
* Elliptic-Curve Cryptography (ECC) key with a size of at least 256 bits  
In addition, the leaf server certificate hashing algorithm must be Secure Hash Algorithm 2 (SHA-2) with a digest length of at least 256 (that is, SHA-256 or greater).  
If ATS is not enabled, the system still performs HTTPS server trust evaluation but you can override it on a case-by-case basis, as described in HTTPS Server Trust Evaluation. With ATS fully enabled, you cannot override the default HTTPS server trust evaluation.  
"""  

### Testing  
There are 2 main ways to test ATS compatability:  
* nscurl: nscurl is a utility added in MAC OS X 10.11 "El Capitan" that runs a ats diagnotics test  
* SSL labs: SSL labs also tests handshake with ATS and can tell you if a server is compatible with ATS  
This tool is a python wrapper around these 2 methods and adds some file I/O to do this in bulk

### How to run this tool  
Download all the files  
Open terminal and run  
python ats_check.py -i input_file_with_inputs  
to test multiple inputs present in newline sperated input file or  
python ats_check.py -u url_to_test  
to test a single url  
The tool will check if it is running on El Capitan or better and use nscurl if it is available(as it is faster than running SSL labs scan) or run SSL labs scan and return the result if it is not available  
After execution, you will see a list of inputs that failed the test printed on the terminal and a new json results file with all the results for future referece  
I've included an input file and corresponding result json file for reference  


### Dependencies
* Python
* nscurl for a quicker test
* Python requests package - pip install requests

### Additional docs  
iOS security guide: http://www.apple.com/business/docs/iOS_Security_Guide.pdf  
ATS requirements doc: https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CocoaKeys.html#//apple_ref/doc/uid/TP40009251-SW35  
List of root CA for iOS: https://support.apple.com/en-us/HT204132  
TLS 1.3 draft: Check draft 2 proposed changes of https://tlswg.github.io/tls13-spec/#rfc.section.1.2 for support for only AEAD modes  
What's new in security talk at WWDC 2016: https://developer.apple.com/videos/play/wwdc2016/706/ first part of the talk is dedicated to ATS  
NSAppTransportSecurity Cocoa key - https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CocoaKeys.html#//apple_ref/doc/uid/TP40009251-SW33  
