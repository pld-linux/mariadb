# TODO:
# - package not conflicting with mysql (or just easily replacing mysql)
# - something wrong in //libmysql/CMakeLists.txt and thus symbols like
#   libmysqlclient.so.18(libmysqlclient_16) are missing
#
# Conditional build:
%bcond_without	innodb		# InnoDB storage engine support
%bcond_without	big_tables	# Support tables with more than 4G rows even on 32 bit platforms
%bcond_with	connect		# Connect Storage Engine
%bcond_without	federated	# Federated Storage Engine support
%bcond_without	raid		# RAID support
%bcond_without	ssl		# OpenSSL support
%bcond_without	tcpd		# libwrap (tcp_wrappers) support
%bcond_without	tokudb		# TokuDB engine support (available only for x86_64 ??)
%bcond_without	mroonga		# https://mariadb.com/kb/en/mariadb/about-mroonga/ (only for x86_64)
%bcond_without	rocksdb		# https://mariadb.com/kb/en/library/about-myrocks-for-mariadb/ (only for x86_64)
%bcond_with	autodeps	# BR packages needed only for resolving deps
%bcond_without	oqgraph		# Open Query GRAPH engine (OQGRAPH)
%bcond_without	sphinx		# Sphinx storage engine support
%bcond_without	cracklib	# cracklib support
%bcond_without	lz4		# lz4 page compression for InnoDB & XtraDB
%bcond_with	tests		# FIXME: don't run correctly
%bcond_with	ndb
%bcond_with	cassandra	# Cassandra Storage Engine (https://jira.mariadb.org/browse/MDEV-21368)

%ifnarch %{x8664}
%unglobal	with_tokudb
%unglobal	with_mroonga
%unglobal	with_rocksdb
%endif

Summary:	An enhanced, drop-in replacement for MySQL
Summary(de.UTF-8):	MariaDB: ist eine SQL-Datenbank
Summary(fr.UTF-8):	MariaDB: un serveur SQL rapide et fiable
Summary(pl.UTF-8):	MariaDB: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR.UTF-8):	MariaDB: Um servidor SQL rápido e confiável
Summary(ru.UTF-8):	MariaDB - быстрый SQL-сервер
Summary(uk.UTF-8):	MariaDB - швидкий SQL-сервер
Summary(zh_CN.UTF-8):	MariaDB数据库服务器
Name:		mariadb
Version:	10.4.12
Release:	0.1
License:	GPL + MariaDB FLOSS Exception
Group:		Applications/Databases
Source0:	https://downloads.mariadb.org/f/%{name}-%{version}/source/%{name}-%{version}.tar.gz
# Source0-md5:	97d7c0f508c04a31c138fdb24e95dbc4
Source100:	http://sphinxsearch.com/files/sphinx-2.2.11-release.tar.gz
# Source100-md5:	5cac34f3d78a9d612ca4301abfcbd666
Source1:	mysql.init
Source2:	mysql.sysconfig
Source3:	mysql.logrotate
Source4:	mysqld.conf
Source5:	mysql-clusters.conf
Source7:	mysql-ndb.init
Source8:	mysql-ndb.sysconfig
Source9:	mysql-ndb-mgm.init
Source10:	mysql-ndb-mgm.sysconfig
Source11:	mysql-ndb-cpc.init
Source12:	mysql-ndb-cpc.sysconfig
Source13:	mysql-client.conf
Patch0:		mysql-client-config.patch
Patch1:		heimdal.patch
Patch2:		build.patch
URL:		https://mariadb.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cmake >= 2.6
%{?with_cracklib:BuildRequires:	cracklib-devel}
BuildRequires:	doxygen
BuildRequires:	groff
BuildRequires:	libbson-devel >= 1.16.0
BuildRequires:	libevent-devel
BuildRequires:	libstdc++-devel >= 5:3.0
BuildRequires:	libtool
%{?with_tcpd:BuildRequires:	libwrap-devel}
%{?with_lz4:BuildRequires:	lz4-devel}
BuildRequires:	ncurses-devel >= 4.2
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_autodeps:BuildRequires:	perl-DBI}
BuildRequires:	perl-devel >= 1:5.6.1
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.414
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
# FIXME: to get thrift-devel 0.9.1 build it without php
%{?with_cassandra:BuildRequires:	thrift-devel >= 0.13}
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post): sed >= 4.0
Requires:	%{name}-charsets = %{version}-%{release}
Requires:	/usr/bin/setsid
Requires:	rc-scripts >= 0.2.0
Provides:	MariaDB-server
Provides:	group(mysql)
Provides:	msqlormysql
Provides:	user(mysql)
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}
%define		_localstatedir	/var/lib/%{name}
%define		_mysqlhome	/home/services/mysql

%define		_noautoreqdep	'perl(DBD::mysql)'

# readline/libedit detection goes wrong
%undefine	configure_cache

%description
Maria Engine is an extended version of MyISAM which is crash safe.

MariaDB is a true multi-user, multi-threaded SQL (Structured Query
Language) database server. SQL is the most popular database language
in the world. MariaDB is a client/server implementation that consists
of a server daemon mysqld and many different client
programs/libraries.

The main goals of MariaDB are speed, robustness and easy to use.
MariaDB was originally developed because we at Tcx needed a SQL server
that could handle very big databases with magnitude higher speed than
what any database vendor could offer to us. We have now been using
MariaDB since 1996 in a environment with more than 40 databases,
10,000 tables, of which more than 500 have more than 7 million rows.
This is about 50G of mission critical data.

The base upon which MariaDB is built is a set of routines that have
been used in a highly demanding production environment for many years.
While MariaDB is still in development, it already offers a rich and
highly useful function set.

%description -l fr.UTF-8
MariaDB est un serveur de bases de donnees SQL vraiment multi-usagers
et multi-taches. Le langage SQL est le langage de bases de donnees le
plus populaire au monde. MariaDB est une implementation client/serveur
qui consiste en un serveur (mysqld) et differents
programmes/bibliotheques clientes.

Les objectifs principaux de MariaDB sont: vitesse, robustesse et
facilite d'utilisation. MariaDB fut originalement developpe parce que
nous, chez Tcx, avions besoin d'un serveur SQL qui pouvait gerer de
tres grandes bases de donnees avec une vitesse d'un ordre de magnitude
superieur a ce que n'importe quel vendeur pouvait nous offrir. Nous
utilisons MariaDB depuis 1996 dans un environnement avec plus de 40
bases de donnees, 10000 tables, desquelles plus de 500 ont plus de 7
millions de lignes. Ceci represente environ 50G de donnees critiques.

A la base de la conception de MariaDB, on retrouve une serie de
routines qui ont ete utilisees dans un environnement de production
pendant plusieurs annees. Meme si MariaDB est encore en developpement,
il offre deja une riche et utile serie de fonctions.

%description -l pl.UTF-8
MariaDB to prawdziwie wieloużytkownikowy, wielowątkowy serwer baz
danych SQL. SQL jest najpopularniejszym na świecie językiem używanym
do baz danych. MariaDB to implementacja klient/serwer składająca się z
demona mysqld i wielu różnych programów i bibliotek klienckich.

Głównymi celami MariaDB-a są szybkość, potęga i łatwość użytkowania.
MariaDB oryginalnie był tworzony, ponieważ autorzy w Tcx potrzebowali
serwera SQL do obsługi bardzo dużych baz danych z szybkością o wiele
większą, niż mogli zaoferować inni producenci baz danych. Używają go
od 1996 roku w środowisku z ponad 40 bazami danych, 10 000 tabel, z
których ponad 500 zawiera ponad 7 milionów rekordów - w sumie około
50GB krytycznych danych.

Baza, na której oparty jest MariaDB, składa się ze zbioru procedur,
które były używane w bardzo wymagającym środowisku produkcyjnym przez
wiele lat. Pomimo, że MariaDB jest ciągle rozwijany, już oferuje
bogaty i użyteczny zbiór funkcji.

%description -l de.UTF-8
MariaDB ist eine SQL-Datenbank. Allerdings ist sie im Gegensatz zu
Oracle, DB2 oder PostgreSQL keine relationale Datenbank. Die Daten
werden zwar in zweidimensionalen Tabellen gespeichert und können mit
einem Primärschlüssel versehen werden. Es ist aber keine Definition
eines Fremdschlüssels möglich. Der Benutzer ist somit bei einer
MariaDB-Datenbank völlig allein für die (referenzielle) Integrität der
Daten verantwortlich. Allein durch die Nutzung externer
Tabellenformate, wie InnoDB bzw Berkeley DB wird eine Relationalität
ermöglicht. Diese Projekte sind aber getrennt von MariaDB zu
betrachten.

%description -l pt_BR.UTF-8
O MariaDB é um servidor de banco de dados SQL realmente multiusuário e
multi-tarefa. A linguagem SQL é a mais popular linguagem para banco de
dados no mundo. O MariaDB é uma implementação cliente/servidor que
consiste de um servidor chamado mysqld e diversos
programas/bibliotecas clientes. Os principais objetivos do MariaDB
são: velocidade, robustez e facilidade de uso. O MariaDB foi
originalmente desenvolvido porque nós na Tcx precisávamos de um
servidor SQL que pudesse lidar com grandes bases de dados e com uma
velocidade muito maior do que a que qualquer vendedor podia nos
oferecer. Estamos usando o MariaDB desde 1996 em um ambiente com mais
de 40 bases de dados com 10.000 tabelas, das quais mais de 500 têm
mais de 7 milhões de linhas. Isto é o equivalente a aproximadamente
50G de dados críticos. A base da construção do MariaDB é uma série de
rotinas que foram usadas em um ambiente de produção com alta demanda
por muitos anos. Mesmo o MariaDB estando ainda em desenvolvimento, ele
já oferece um conjunto de funções muito ricas e úteis. Veja a
documentação para maiores informações.

%description -l ru.UTF-8
MariaDB - это SQL (Structured Query Language) сервер базы данных.
MariaDB была написана Michael'ом (monty) Widenius'ом. См. файл CREDITS
в дистрибутиве на предмет других участников проекта и прочей
информации о MariaDB.

%description -l uk.UTF-8
MariaDB - це SQL (Structured Query Language) сервер бази даних.
MariaDB було написано Michael'ом (monty) Widenius'ом. Див. файл
CREDITS в дистрибутиві для інформації про інших учасників проекту та
іншої інформації.

%package charsets
Summary:	MariaDB - character sets definitions
Summary(pl.UTF-8):	MariaDB - definicje kodowań znaków
Group:		Applications/Databases

%description charsets
This package contains character sets definitions needed by both client
and server.

%description charsets -l pl.UTF-8
Ten pakiet zawiera definicje kodowań znaków potrzebne dla serwera i
klienta.

%package extras
Summary:	MariaDB additional utilities
Summary(pl.UTF-8):	Dodatkowe narzędzia do MariaDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description extras
MariaDB additional utilities except Perl scripts (they may be found in
mysql-extras-perl package).

%description extras -l pl.UTF-8
Dodatkowe narzędzia do MariaDB - z wyjątkiem skryptów Perla (które są
w pakiecie mysql-extras-perl).

%package extras-perl
Summary:	MariaDB additional utilities written in Perl
Summary(pl.UTF-8):	Dodatkowe narzędzia do MariaDB napisane w Perlu
Group:		Applications/Databases
Requires:	%{name}-extras = %{version}-%{release}
Requires:	perl-DBD-mysql

%description extras-perl
MariaDB additional utilities written in Perl.

%description extras-perl -l pl.UTF-8
Dodatkowe narzędzia do MariaDB napisane w Perlu.

%package client
Summary:	MariaDB - Client
Summary(pl.UTF-8):	MariaDB - Klient
Summary(pt.UTF-8):	MariaDB - Cliente
Summary(ru.UTF-8):	MariaDB клиент
Summary(uk.UTF-8):	MariaDB клієнт
Group:		Applications/Databases
Requires:	%{name}-charsets = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description client
This package contains the standard MariaDB clients.

%description client -l fr.UTF-8
Ce package contient les clients MariaDB standards.

%description client -l pl.UTF-8
Standardowe programy klienckie MariaDB.

%description client -l pt_BR.UTF-8
Este pacote contém os clientes padrão para o MariaDB.

%description client -l ru.UTF-8
Этот пакет содержит только клиент MariaDB.

%description client -l uk.UTF-8
Цей пакет містить тільки клієнта MariaDB.

%package libs
Summary:	Shared libraries for MariaDB/MySQL clients
Summary(pl.UTF-8):	Biblioteki dzielone MariaDB
Group:		Libraries

%description libs
Shared libraries for any MariaDB/MySQL client program or interface.

%description libs -l pl.UTF-8
Biblioteki dzielone MariaDB.

%package devel
Summary:	Files for development of MariaDB/MySQL applications
Summary(pl.UTF-8):	MariaDB - Pliki nagłówkowe i biblioteki dla programistów
Summary(pt.UTF-8):	MariaDB - Medições de desempenho
Summary(ru.UTF-8):	MariaDB - хедеры и библиотеки разработчика
Summary(uk.UTF-8):	MariaDB - хедери та бібліотеки програміста
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_ssl:Requires: openssl-devel}
Requires:	zlib-devel

%description devel
This package contains the libraries and header files that are needed
for developing MariaDB/MySQL client applications.

%description devel -l fr.UTF-8
Ce package contient les fichiers entetes et les librairies de
developpement necessaires pour developper des applications clientes
MariaDB.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki konieczne do kompilacji aplikacji
klienckich MariaDB.

%description devel -l pt_BR.UTF-8
Este pacote contém os arquivos de cabeçalho (header files) e
bibliotecas necessárias para desenvolver aplicações clientes do
MariaDB.

%description devel -l ru.UTF-8
Этот пакет содержит хедеры и библиотеки разработчика, необходимые для
разработки клиентских приложений.

%description devel -l uk.UTF-8
Цей пакет містить хедери та бібліотеки програміста, необхідні для
розробки програм-клієнтів.

%package static
Summary:	MariaDB static libraries
Summary(pl.UTF-8):	Biblioteki statyczne MariaDB
Summary(ru.UTF-8):	MariaDB - статические библиотеки
Summary(uk.UTF-8):	MariaDB - статичні бібліотеки
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
MariaDB static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne MariaDB.

%description static -l ru.UTF-8
Этот пакет содержит статические библиотеки разработчика, необходимые
для разработки клиентских приложений.

%description static -l uk.UTF-8
Цей пакет містить статичні бібліотеки програміста, необхідні для
розробки програм-клієнтів.

%package bench
Summary:	MariaDB - Benchmarks
Summary(pl.UTF-8):	MariaDB - Programy testujące szybkość działania bazy
Summary(pt.UTF-8):	MariaDB - Medições de desempenho
Summary(ru.UTF-8):	MariaDB - бенчмарки
Summary(uk.UTF-8):	MariaDB - бенчмарки
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-client
Requires:	perl-DBD-mysql

%description bench
This package contains MariaDB benchmark scripts and data.

%description bench -l pl.UTF-8
Programy testujące szybkość serwera MariaDB.

%description bench -l pt_BR.UTF-8
Este pacote contém medições de desempenho de scripts e dados do
MariaDB.

%description bench -l ru.UTF-8
Этот пакет содержит скрипты и данные для оценки производительности
MariaDB.

%description bench -l uk.UTF-8
Цей пакет містить скрипти та дані для оцінки продуктивності MariaDB.

%package doc
Summary:	MariaDB manual
Summary(pl.UTF-8):	Podręcznik użytkownika MariaDB
Group:		Applications/Databases

%description doc
This package contains manual in HTML format.

%description doc -l pl.UTF-8
Podręcznik MariaDB-a w formacie HTML.

%package ndb
Summary:	MariaDB - NDB Storage Engine Daemon
Summary(pl.UTF-8):	MariaDB - demon silnika przechowywania danych NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb
This package contains the standard MariaDB NDB Storage Engine Daemon.

%description ndb -l pl.UTF-8
Ten pakiet zawiera standardowego demona silnika przechowywania danych
NDB.

%package ndb-client
Summary:	MariaDB - NDB Clients
Summary(pl.UTF-8):	MariaDB - programy klienckie NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-client
This package contains the standard MariaDB NDB Clients.

%description ndb-client -l pl.UTF-8
Ten pakiet zawiera standardowe programy klienckie MariaDB NDB.

%package ndb-mgm
Summary:	MariaDB - NDB Management Daemon
Summary(pl.UTF-8):	MariaDB - demon zarządzający NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-mgm
This package contains the standard MariaDB NDB Management Daemon.

%description ndb-mgm -l pl.UTF-8
Ten pakiet zawiera standardowego demona zarządzającego MariaDB NDB.

%package ndb-cpc
Summary:	MariaDB - NDB CPC Daemon
Summary(pl.UTF-8):	MariaDB - demon NDB CPC
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-cpc
This package contains the standard MariaDB NDB CPC Daemon.

%description ndb-cpc -l pl.UTF-8
Ten pakiet zawiera standardowego demona MariaDB NDB CPC.

%package embedded
Summary:	MariaDB as an embeddable library
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description embedded
This package contains a version of the MariaDB server that can be
embedded into a client application instead of running as a separate
process.

%prep
%setup -q %{?with_sphinx:-a100}
%if %{with sphinx}
mv sphinx-*/mysqlse storage/sphinx
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
# NOTE that /var/lib/mariadb/mariadb.sock is symlink to real sock file
# (it defaults to first cluster but user may change it to whatever
# cluster it wants)

%cmake \
	-DCMAKE_BUILD_TYPE=%{!?debug:RelWithDebInfo}%{?debug:Debug} \
	-DFEATURE_SET="community" \
	-DCMAKE_C_FLAGS="%{rpmcflags} %{rpmcppflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DCMAKE_CXX_FLAGS="%{rpmcxxflags} %{rpmcppflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DWITH_MYSQLD_LDFLAGS="%{rpmldflags}" \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
	-DDAEMON_NAME="%{name}" \
	-DDAEMON_NO_PREFIX="%{name}" \
	-DPLUGIN_CASSANDRA=%{?with_cassandra:DYNAMIC}%{!?with_cassandra:NO} \
	-DPLUGIN_CONNECT=%{?with_connect:DYNAMIC}%{!?with_connect:NO} \
	-DPLUGIN_MROONGA=%{?with_mroonga:DYNAMIC}%{!?with_mroonga:NO} \
	-DPLUGIN_OQGRAPH=%{?with_oqgraph:DYNAMIC}%{!?with_oqgraph:NO} \
	-DPLUGIN_CRACKLIB_PASSWORD_CHECK=%{?with_cracklib:DYNAMIC}%{!?with_cracklib:NO} \
	-DPLUGIN_ROCKSDB=%{?with_rocksdb:DYNAMIC}%{!?with_rocksdb:NO} \
	-DPLUGIN_SPHINX=%{?with_sphinx:DYNAMIC}%{!?with_sphinx:NO} \
	-DPLUGIN_TOKUDB=%{?with_tokudb:DYNAMIC}%{!?with_tokudb:NO} \
	-DPLUGIN_CONNECT=%{?with_connect:DYNAMIC}%{!?with_connect:NO} \
	-DPLUGIN_CLIENT_ED25519=OFF \
	-DPYTHON_SHEBANG=%{python_path} \
	-DPLUGIN_CACHING_SHA2_PASSWORD=%{?with_clibrary:DYNAMIC}%{!?with_clibrary:OFF} \
	-DPLUGIN_AWS_KEY_MANAGEMENT=NO \
        -DPYTHON_SHEBANG=%{__python3} \
	-DENABLED_LOCAL_INFILE=ON \
	-DSECURITY_HARDENED=ON \
	%{?debug:-DWITH_DEBUG=ON} \
	-DWITH_FAST_MUTEXES=ON \
	-DLZ4_LIBS=%{_libdir}/liblz4.so \
	-DLZ4_LIBS=%{?with_lz4:%{_libdir}/liblz4.so}%{!?with_lz4:} \
	-DWITH_INNODB_LZ4=%{?with_lz4:ON}%{!?with_lz4:OFF} \
	-DWITH_ROCKSDB_LZ4=%{?with_lz4:ON}%{!?with_lz4:OFF} \
	-DWITH_PIC=ON \
	-DWITH_LIBEDIT=OFF \
	-DWITH_SSL=%{?with_ssl:system}%{!?with_ssl:no} \
	-DWITH_ZLIB=system \
	-DWITH_PCRE=ON \
	-DWITH_READLINE=ON \
	-DWITH_EMBEDDED_SERVER=ON \
	-DNICE_PROJECT_NAME="MariaDB" \
	-DCOMPILATION_COMMENT="PLD/Linux Distribution MariaDB RPM" \
	-DWITH_LIBWRAP=%{?with_tcpd:ON}%{!?with_tcpd:OFF} \
	-DWITH_UNIT_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
	-DMYSQL_UNIX_ADDR=/var/lib/%{name}/%{name}.sock \
	-DINSTALL_LAYOUT=RPM \
	-DINSTALL_MYSQLTESTDIR_RPM="" \
	-DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir}/%{name} \
	-DINSTALL_SYSCONFDIR=%{_sysconfdir}/%{name} \
	-DINSTALL_SQLBENCHDIR=%{_datadir} \
	-DINSTALL_SUPPORTFILESDIR=%{_datadir}/%{name}-support \
	-DINSTALL_PLUGINDIR=%{_libdir}/%{name}/plugin \
	-DINSTALL_LIBDIR=%{_lib} \
	-DCONNECT_WITH_MONGO=OFF \
	-DCONNECT_WITH_JDBC=OFF \
	..

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig,%{name},skel} \
	   $RPM_BUILD_ROOT/var/{log/{archive,}/%{name},lib/%{name}} \
	   $RPM_BUILD_ROOT{%{_infodir},%{_mysqlhome}} \
	   $RPM_BUILD_ROOT%{_libdir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p Docs/mysql.info $RPM_BUILD_ROOT%{_infodir}

# we use our own
rm $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/logrotate.d/mysql

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/mysql
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/mysql
# This is template for configuration file which is created after 'service mysql init'
cp -p %{SOURCE4} mysqld.conf
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/clusters.conf
touch $RPM_BUILD_ROOT/var/log/%{name}/{mysqld,query,slow}.log

# remove innodb directives from mysqld.conf if mysqld is configured without
%if %{without innodb}
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/innodb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

cp -p mysqld.conf $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld.conf
cp -p %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/mysql-client.conf

# NDB
%if %{with ndb}
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb
cp -p %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb
install -p %{SOURCE9} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb-mgm
cp -p %{SOURCE10} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb-mgm
install -p %{SOURCE11} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb-cpc
cp -p %{SOURCE12} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb-cpc
%endif

# symlinks point to the .so file, fix it
ln -sf libmysqlclient.so.18 $RPM_BUILD_ROOT%{_libdir}/libmysqlclient_r.so.18
ln -sf libmysqlclient.so.18.0.0 $RPM_BUILD_ROOT%{_libdir}/libmysqlclient_r.so.18.0.0

sed -i -e 's,/usr//usr,%{_prefix},g' $RPM_BUILD_ROOT%{_bindir}/mysql_config
sed -i -e '/libs/s/$ldflags//' $RPM_BUILD_ROOT%{_bindir}/mysql_config

# remove known unpackaged files
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}-support

# rename not to be so generic name
mv $RPM_BUILD_ROOT%{_bindir}/{,mysql_}resolve_stack_dump
mv $RPM_BUILD_ROOT%{_mandir}/man1/{,mysql_}resolve_stack_dump.1

# not useful without -debug build
%{!?debug:%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysql_resolve_stack_dump}
%{!?debug:%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql_resolve_stack_dump.1}
# generate symbols file, so one can generate backtrace using it
# mysql_resolve_stack_dump -s %{_datadir}/%{name}/mysqld.sym -n mysqld.stack.
# http://dev.mysql.com/doc/refman/5.0/en/using-stack-trace.html
%{?debug:nm -n $RPM_BUILD_ROOT%{_sbindir}/mysqld > $RPM_BUILD_ROOT%{_datadir}/%{name}/mysqld.sym}

# do not clobber users $PATH
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_plugin
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_upgrade
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/innochecksum
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisamchk
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisamlog
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisampack
#mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_fix_privilege_tables
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/my_print_defaults
sed -i -e 's#/usr/bin/my_print_defaults#%{_sbindir}/my_print_defaults#g' $RPM_BUILD_ROOT%{_bindir}/mysql_install_db
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysqlcheck

# delete - functionality in initscript / rpm
# note: mysql_install_db (and thus resolveip) are needed by digikam
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysqld_safe
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysqld_multi
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysqld_{multi,safe}*
#rm $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql-log-rotate
#rm $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql.server
#rm $RPM_BUILD_ROOT%{_datadir}/%{name}/binary-configure
%{__rm} $RPM_BUILD_ROOT%{_datadir}/mysql/errmsg-utf8.txt
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysql_waitpid
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql_waitpid.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql.server*
#%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysqlman.1*
#%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/comp_err.1*

# we don't package those (we have no -test or -testsuite pkg) and some of them just segfault
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysql_client_test
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql_client_test.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql_client_test_embedded.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql-stress-test.pl.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql-test-run.pl.1*
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/mysql-test

# mariadb groff symlink to oracle mysql man pages
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{mariadb-client-test-embedded,mariadb-client-test,mariadb-waitpid,mariadbd-multi,mariadbd-safe,mariadbd-safe-helper}.1

# not needed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/libdaemon_example.*

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 89 mysql
%useradd -u 89 -d %{_mysqlhome} -s /bin/sh -g mysql -c "MariaDB Server" mysql

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add mysql
%service mysql restart

%preun
if [ "$1" = "0" ]; then
	%service -q mysql stop
	/sbin/chkconfig --del mysql
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

if [ "$1" = "0" ]; then
	%userremove mysql
	%groupremove mysql
fi

%post ndb
/sbin/chkconfig --add mysql-ndb
%service mysql-ndb restart "mysql NDB engine"

%preun ndb
if [ "$1" = "0" ]; then
	%service mysql-ndb stop
	/sbin/chkconfig --del mysql-ndb
fi

%post ndb-mgm
/sbin/chkconfig --add mysql-ndb-mgm
%service mysql-ndb-mgm restart "mysql NDB management node"

%preun ndb-mgm
if [ "$1" = "0" ]; then
	%service mysql-ndb-mgm stop
	/sbin/chkconfig --del mysql-ndb-mgm
fi

%post ndb-cpc
/sbin/chkconfig --add mysql-ndb-cpc
%service mysql-ndb-cpc restart "mysql NDB CPC"

%preun ndb-cpc
if [ "$1" = "0" ]; then
	%service mysql-ndb-cpc stop
	/sbin/chkconfig --del mysql-ndb-cpc
fi

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post	embedded -p /sbin/ldconfig
%postun	embedded -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc KNOWN_BUGS.txt README.md CREDITS COPYING THIRDPARTY
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mysql
%attr(754,root,root) /etc/rc.d/init.d/mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql
%attr(640,root,mysql) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/clusters.conf
%attr(755,root,root) %{_sbindir}/innochecksum
%attr(755,root,root) %{_sbindir}/myisamchk
%attr(755,root,root) %{_sbindir}/myisamlog
%attr(755,root,root) %{_sbindir}/myisampack
%attr(755,root,root) %{_sbindir}/my_print_defaults
%attr(755,root,root) %{_sbindir}/mysqlcheck
%attr(755,root,root) %{_sbindir}/mysqld
#%attr(755,root,root) %{_sbindir}/mysql_fix_privilege_tables
%attr(755,root,root) %{_sbindir}/mysql_upgrade
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugin
%{_libdir}/%{name}/plugin/daemon_example.ini
%attr(755,root,root) %{_libdir}/%{name}/plugin/adt_null.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_0x0100.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_pam.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_test_plugin.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/dialog.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/dialog_examples.so
#%attr(755,root,root) %{_libdir}/%{name}/plugin/feedback.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_federated.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/handlersocket.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/mypluglib.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/mysql_clear_password.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_client.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_interface.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_server.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/query_cache_info.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/sql_errlog.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_spider.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_example.so
%if %{with tokudb}
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_tokudb.so
%endif
%if %{with cassandra}
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_cassandra.so
%endif
%attr(755,root,root) %{_libdir}/%{name}/plugin/locales.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/metadata_lock_info.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/query_response_time.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/server_audit.so

#%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_archive.so
#%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_blackhole.so
#%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_federatedx.so
#%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_connect.so
#%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_sequence.so
#%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_test_sql_discovery.so
%if %{with sphinx}
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_sphinx.so
%endif

%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/mysqlcheck.1*
#%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysql_plugin.1*
%{_mandir}/man8/mysqld.8*

%if %{?debug:1}0
%attr(755,root,root) %{_bindir}/*resolve_stack_dump
%{_datadir}/mysql/mysqld.sym
%{_mandir}/man1/*resolve_stack_dump.1*
%endif

#%dir %{_docdir}/%{name}-%{version}
#%attr(644,root,root) %{_docdir}/%{name}-%{version}/*

%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/my.cnf
%dir %{_sysconfdir}/my.cnf.d
%{_sysconfdir}/my.cnf.d/client.cnf
%{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%{_sysconfdir}/my.cnf.d/server.cnf
%if %{with tokudb}
#%{_sysconfdir}/my.cnf.d/tokudb.cnf
%endif
%attr(755,root,root) %{_bindir}/mysql_install_db
%attr(755,root,root) %{_bindir}/mytop
%attr(755,root,root) %{_bindir}/resolveip
%attr(755,root,root) %{_sbindir}/mysql_plugin
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/resolveip.1*

%attr(700,mysql,mysql) %{_mysqlhome}
# root:root is proper here for mysql.rpm while mysql:mysql is potential security hole
#%attr(751,root,root) /var/lib/mysql
%attr(750,mysql,mysql) %dir /var/log/%{name}
%attr(750,mysql,mysql) %dir /var/log/archive/%{name}
%attr(640,mysql,mysql) %ghost /var/log/%{name}/*

%{_infodir}/mysql.info*
# This is template for configuration file which is created after 'service mysql init'
%{_datadir}/mysql/mysqld.conf
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/mysql_performance_tables.sql
%{_datadir}/mysql/install_spider.sql

%{_datadir}/mysql/english
%{_datadir}/mysql/fill_help_tables.sql
#%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(es) %{_datadir}/mysql/spanish
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(nl) %{_datadir}/mysql/dutch
%lang(nb) %{_datadir}/mysql/norwegian
%lang(nn) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sk) %{_datadir}/mysql/slovak
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian

%files charsets
%defattr(644,root,root,755)
%dir %{_datadir}/mysql
%{_datadir}/mysql/charsets

%files extras
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aria_chk
%attr(755,root,root) %{_bindir}/aria_dump_log
%attr(755,root,root) %{_bindir}/aria_ftdump
%attr(755,root,root) %{_bindir}/aria_pack
%attr(755,root,root) %{_bindir}/aria_read_log
%attr(755,root,root) %{_bindir}/msql2mysql
%attr(755,root,root) %{_bindir}/myisam_ftdump
%attr(755,root,root) %{_bindir}/mysql_secure_installation
%attr(755,root,root) %{_bindir}/mysql_tzinfo_to_sql
%attr(755,root,root) %{_bindir}/perror
%attr(755,root,root) %{_bindir}/replace
%if %{with tokudb}
%attr(755,root,root) %{_bindir}/tokuftdump
%endif
%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*

%files extras-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysqlaccess
%attr(755,root,root) %{_bindir}/mysql_convert_table_format
%attr(755,root,root) %{_bindir}/mysqldumpslow
%attr(755,root,root) %{_bindir}/mysql_find_rows
%attr(755,root,root) %{_bindir}/mysql_fix_extensions
%attr(755,root,root) %{_bindir}/mysqlhotcopy
%attr(755,root,root) %{_bindir}/mysql_setpermission
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysql_setpermission.1*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql
%attr(755,root,root) %{_bindir}/mysqladmin
%attr(755,root,root) %{_bindir}/mysqlbinlog
%attr(755,root,root) %{_bindir}/mysqldump
%attr(755,root,root) %{_bindir}/mysqlimport
%attr(755,root,root) %{_bindir}/mysqlshow
%attr(755,root,root) %{_bindir}/mysqlslap
#%attr(755,root,root) %{_sbindir}/mysqlmanager
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlimport.1*
#%{_mandir}/man1/mysqlmanagerc.1*
#%{_mandir}/man1/mysqlmanager-pwgen.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
#%{_mandir}/man8/mysqlmanager.8*

%files libs
%defattr(644,root,root,755)
%doc EXCEPTIONS-CLIENT
%attr(751,root,root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/mysql-client.conf
%attr(755,root,root) %{_libdir}/libmysqlclient_r.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmysqlclient_r.so.18
%if %{with ndb}
%attr(755,root,root) %{_libdir}/libndbclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndbclient.so.3
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_config
%attr(755,root,root) %{_libdir}/lib*.so
#%{_libdir}/lib*.la
%{_libdir}/lib*[!tr].a
%{_includedir}/mysql
%{_aclocaldir}/mysql.m4
%{_mandir}/man1/mysql_config.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*[tr].a

%files bench
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysqltest
%dir %{_datadir}/sql-bench
%{_datadir}/sql-bench/[CDRl]*
%{_datadir}/sql-bench/myisam.cnf
%attr(755,root,root) %{_datadir}/sql-bench/[bcgirst]*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/mysqltest_embedded.1*

%if %{with ndb}
%files ndb
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndbd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb
#%{_mandir}/man1/ndbd.1*
%{_mandir}/man1/ndbd_redo_log_reader.1*

%files ndb-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ndb_config
%attr(755,root,root) %{_bindir}/ndb_delete_all
%attr(755,root,root) %{_bindir}/ndb_desc
%attr(755,root,root) %{_bindir}/ndb_drop_index
%attr(755,root,root) %{_bindir}/ndb_drop_table
%attr(755,root,root) %{_bindir}/ndb_error_reporter
%attr(755,root,root) %{_bindir}/ndb_mgm
%attr(755,root,root) %{_bindir}/ndb_print_backup_file
%attr(755,root,root) %{_bindir}/ndb_print_schema_file
%attr(755,root,root) %{_bindir}/ndb_print_sys_file
%attr(755,root,root) %{_bindir}/ndb_restore
%attr(755,root,root) %{_bindir}/ndb_select_all
%attr(755,root,root) %{_bindir}/ndb_select_count
%attr(755,root,root) %{_bindir}/ndb_show_tables
%attr(755,root,root) %{_bindir}/ndb_size.pl
%attr(755,root,root) %{_bindir}/ndb_test_platform
%attr(755,root,root) %{_bindir}/ndb_waiter
%{_mandir}/man1/ndb_config.1*
%{_mandir}/man1/ndb_delete_all.1*
%{_mandir}/man1/ndb_desc.1*
%{_mandir}/man1/ndb_drop_index.1*
%{_mandir}/man1/ndb_drop_table.1*
%{_mandir}/man1/ndb_error_reporter.1*
%{_mandir}/man1/ndb_mgm.1*
%{_mandir}/man1/ndb_print_backup_file.1*
%{_mandir}/man1/ndb_print_schema_file.1*
%{_mandir}/man1/ndb_print_sys_file.1*
%{_mandir}/man1/ndb_restore.1*
%{_mandir}/man1/ndb_select_all.1*
%{_mandir}/man1/ndb_select_count.1*
%{_mandir}/man1/ndb_show_tables.1*
%{_mandir}/man1/ndb_size.pl.1*
%{_mandir}/man1/ndb_waiter.1*

%files ndb-mgm
%defattr(644,root,root,755)
#%attr(755,root,root) %{_sbindir}/ndb_mgmd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb-mgm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb-mgm
#%{_mandir}/man1/ndb_mgmd.1*

%files ndb-cpc
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_cpcd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb-cpc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb-cpc
%{_mandir}/man1/ndb_cpcd.1*
%endif

%files embedded
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_client_test_embedded
%attr(755,root,root) %{_bindir}/mysql_embedded
%attr(755,root,root) %{_bindir}/mysqltest_embedded
