Summary:	mcclient - MCCP mud proxy	
Name:		mcclient
Version:	0.4
Release:	1
License:	GPL v2
Group:		Applications/Games
Source0:	http://www.randomly.org/projects/MCCP/%{name}-%{version}.tar.gz
# Source0-md5:	0f56cc75edcf6602a11b878edd3190f0
BuildRequires:	zlib-devel
Requires:	zlib
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mcclient performs decompression of the mud client compression protocol.
This protocol allows the mud to compress all data it sends to you. This
reduces the bandwidth used by the mud (and bandwidth costs money). It
also tends to speed up your mud connection somewhat - less data is
sent, so packet loss is less likely, and large output can actually get
there faster.

%prep
%setup -q 

mv -f mcclient.cfg mcclient.cfg.orig
cat << EOF >> mcclient.cfg
4445 arkadia.rpg.pl 23
4446 barsawia.uni.cc 23
EOF
cat mcclient.cfg.orig >> mcclient.cfg

%build
%{__make} linux

%install
rm -rf $RPM_BUILD_ROOT
install -d linux $RPM_BUILD_ROOT%{_bindir}
install linux/mcclient $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.protocol README.source mcclient.cfg
%attr(755,root,root) "%{_bindir}/*"
