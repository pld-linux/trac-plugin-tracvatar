%define		trac_ver	0.12
%define		plugin		tracvatar
Summary:	Adds Gravatar icons to Trac
Name:		trac-plugin-%{plugin}
Version:	1.7
Release:	1
License:	MIT
Group:		Applications/WWW
Source0:	https://bitbucket.org/zzzeek/tracvatar/get/rel_1_7.tar.bz2
# Source0-md5:	2a9477232efe7af3d6523dc63c57e917
URL:		https://bitbucket.org/zzzeek/tracvatar
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		trac_htdocs		/usr/share/trac/htdocs
%define		plugin_htdocs	%{trac_htdocs}/%{plugin}

%description
Currently, only Gravatar is supported, but the more open-ended plugin
system of Hackergotchi can be re-implemented here if other avatar
engines are desired.

Ideally, Trac itself would just include support for author avatars as
a built in, since this is an extremely common and desirable feature.

For now, the approach of the plugin is to filter specific Trac views,
gather all the authors found in the "data" hash being passed to
Genshi, then using Genshi filters to insert additional Gravatar nodes.

Currently supported views are:
- Timeline
- Issue display
- Issue change display (i.e. comments, attachments)
- Source browser listing (tested for svn and hg so far)
- Individual changeset page (tested for svn and hg so far)
- User prefs page (includes link to "change your avatar" at
  gravatar.com)

%prep
%setup -qc
mv zzzeek-tracvatar-*/* .

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{plugin_htdocs}
mv $RPM_BUILD_ROOT{%{py_sitescriptdir}/tracvatar/htdocs/*,%{plugin_htdocs}}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin tracvatar.web_ui.avatarmodule

%files
%defattr(644,root,root,755)
%doc README.rst CHANGES LICENSE
%dir %{py_sitescriptdir}/tracvatar
%{py_sitescriptdir}/tracvatar/*.py[co]
%{py_sitescriptdir}/tracvatar-%{version}-*.egg-info
%{plugin_htdocs}
