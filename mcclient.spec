Summary:	mcclient - MCCP mud proxy
Summary(pl.UTF-8):   mcclient - proxy do mudów z MCCP
Name:		mcclient
Version:	0.4
Release:	2
License:	GPL v2
Group:		Applications/Games
Source0:	http://www.randomly.org/projects/MCCP/%{name}-%{version}.tar.gz
# Source0-md5:	0f56cc75edcf6602a11b878edd3190f0
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-paths.patch
BuildRequires:	zlib-devel
Requires(post,preun):   /sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mcclient performs decompression of the mud client compression
protocol. This protocol allows the mud to compress all data it sends
to you. This reduces the bandwidth used by the mud (and bandwidth
costs money). It also tends to speed up your mud connection somewhat -
less data is sent, so packet loss is less likely, and large output can
actually get there faster.

%description -l pl.UTF-8
Mcclient przeprowadza dekompresję wykorzystując protokół MCCP.
Protokół ten umożliwia kompresję wszystkich danych wysyłanych przez
muda do klienta. Zmniejsza to obciążenie łącza - mniej danych jest
wysyłanych, co przy dużej liczbie klientów może znacząco wpłynąć na
komfort gry.

%prep
%setup -q
%patch0 -p0

mv -f mcclient.cfg mcclient.cfg.orig
cat >> mcclient.cfg << EOF
4445 arkadia.rpg.pl 23
4446 barsawia.uni.cc 23
EOF
cat mcclient.cfg.orig >> mcclient.cfg

%build
%{__make} linux

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/{rc.d/init.d,sysconfig}}

install linux/mcclient $RPM_BUILD_ROOT%{_bindir}
install mcclient.cfg $RPM_BUILD_ROOT%{_sysconfdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mcclient
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/mcclient

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mcclient
if [ -f /var/lock/subsys/mcclient ]; then
        /etc/rc.d/init.d/mcclient restart 1>&2
	else
	echo "Do not forget to edit /etc/mcclient.cfg"
        echo "Run '/etc/rc.d/init.d/mcclient start' to start mcclient."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mcclient ]; then
		/etc/rc.d/init.d/mcclient stop 1>&2
	fi
        /sbin/chkconfig --del mcclient
fi

%files
%defattr(644,root,root,755)
%doc README.protocol README.source
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/mcclient
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mcclient
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mcclient.cfg
