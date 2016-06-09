#
# spec file for package hawk
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
# --------- Definition section ----------
# For all macros for opensuse, look at /usr/lib/rpm/macro (global RPM configuration file)
%if 0%{?suse_version} # DOCS: If the value after expansion is different from 0 then is true, otherwise if {?suse_version} is not define, 0%{?suse_version} after expansion will be 0, see http://unix.stackexchange.com/questions/145999/rpm-macros-on-centos-6-5 && http://lists.rpm.org/pipermail/rpm-list/2009-January/000140.html && https://en.opensuse.org/openSUSE:Build_Service_cross_distribution_howto
# DOCS: Defining some macros, see http://www.rpm.org/wiki/PackagerDocs/Macros
%define	www_base	/srv/www
%define	vendor_ruby	vendor_ruby
%define	init_style	suse
%define	pkg_group	Productivity/Clustering/HA
%else
%define	www_base	/var/www
%define	vendor_ruby	site_ruby
%define	init_style	redhat
%define	pkg_group	System Environment/Daemons
%endif

%define	gname		haclient
%define	uname		hacluster
# -------- END Definition section ------
# Rpm tags: http://www.rpm.org/max-rpm/s1-rpm-inside-tags.html
Name:           hawk
Summary:        HA Web Konsole
License:        GPL-2.0
Group:          %{pkg_group}
Version:        2.0.0
Release:        0
Url:            http://www.clusterlabs.org/wiki/Hawk
Source:         %{name}-%{version}.tar.bz2 # DOCS: This line points at the HOME location of the pristine source file. It is used if you ever want to get the source again or check for newer versions. Caveat: The filename in this line MUST match the filename you have on your own system (ie. don't download the source file and change its name). These files would go in the SOURCES directory. These files would go in the SOURCES directory.
Source100:      hawk-rpmlintrc # DOCS: Used to deal with rpmlint warnings and errors, see https://old-en.opensuse.org/Packaging/RpmLint#RPM_Lint to understand rpmlint
BuildRoot:      %{_tmppath}/%{name}-%{version}-build # DOCS: %_tmppath is	/var/tmp,  This line allows you to specify a directory as the "root" for building and installing the new package.
Provides:       ha-cluster-webui # DOCS: The provides tag is used to specify a virtual package that the packaged software makes available when it is installed. Normally, this tag would be used when different packages provide equivalent services. For example, any package that allows a user to read mail might provide the mail-reader virtual package. Another package that depends on a mail reader of some sort, could require the mail-reader virtual package. It would then install without dependency problems, if any one of several mail programs were installed.
Requires:       crmsh # DOCS: The requires tag is used to alert RPM to the fact that the package needs to have certain capabilities available in order to operate properly. These capabilities refer to the name of another package, or to a virtual package provided by one or more packages that use the provides tag. When the requires tag references a package name, version comparisons may also be included by following the package name with <, >, =, >=, or <=, and a version specification. To get even more specific, a package's release may be included as well.
Requires:       graphviz # ToUnderstand: used for rendering the transition schema
Requires:       graphviz-gd
# Need a font of some kind for graphviz to work correctly (bsc#931950)
Requires:       dejavu # DOCS: The DejaVu fonts are a font family based on the Bitstream Vera Fonts.
Requires:       pacemaker >= 1.1.8
%if 0%{?fedora_version} >= 19
Requires:       rubypick # DOCS: Fedora /usr/bin/ruby stub to allow choosing Ruby runtime. Similarly to rbenv or RVM, it allows non-privileged user to choose which is preferred Ruby runtime for current task.
BuildRequires:  rubypick # DOCS: Requires is for the built rpm, BuildRequires is what is required to build, EX: BuildRequires: gcc >= 3 BuildRequires: make Requires: MySQL = 3.23
%endif
Requires:       rubygem(%{rb_default_ruby_abi}:bundler) # DOCS: please see https://en.opensuse.org/openSUSE:Packaging_Ruby#How_gem_dependencies_are_automatically_handled to understand how rpm resolve ruby version
%if 0%{?suse_version}
Recommends:     graphviz-gnome # ToUnderstand, what's the meaning of recommends
Requires:       iproute2
PreReq:         permissions # TODO: (see http://www.rpm.org/max-rpm-snapshot/s1-rpm-depend-manual-dependencies.html) The PreReq tag is the same as Requires, originally with one additional property. Using it used to tell RPM that the package marked as PreReq should be installed before the package containing the dependency. However, as of RPM version 4.4, this special property is being phased out, and PreReq and Requires will soon have no functional differences. A plain Requires is enough to ensure proper installation order if there are no dependency loops present in the transaction. If dependency loops are present and cannot be avoided, packagers should strive to construct them in a way that the order of installation of the the this way interdependent packages does not matter. Historically, in dependency loops PreReq used to "win" over the conventional Requires when RPM determined the installation order in a transaction. But as said above, this functionality is being phased out, and one should no longer assume things will work that way.
BuildRequires:  fdupes
BuildRequires:  libpacemaker-devel
%{?systemd_requires} # DOCS: https://fedoraproject.org/wiki/Packaging:Scriptlets#Scriptlets
%if 0%{?suse_version} >= 1210
BuildRequires:  systemd
%endif
%else
Requires:       iproute
BuildRequires:  pacemaker-libs-devel
%endif
# For build, rpm uses BuildRequires tag, for install, it uses requires, see http://unix.stackexchange.com/questions/40372/how-to-link-requires-to-buildrequires-in-rpm-spec
BuildRequires:  rubygem(%{rb_default_ruby_abi}:builder) >= 3.2
BuildRequires:  rubygem(%{rb_default_ruby_abi}:byebug) >= 3.5
BuildRequires:  rubygem(%{rb_default_ruby_abi}:fast_gettext) >= 0.9.2
BuildRequires:  rubygem(%{rb_default_ruby_abi}:gettext:3) >= 3.1
BuildRequires:  rubygem(%{rb_default_ruby_abi}:gettext_i18n_rails:1) >= 1.2
BuildRequires:  rubygem(%{rb_default_ruby_abi}:gettext_i18n_rails_js) >= 1.0
BuildRequires:  rubygem(%{rb_default_ruby_abi}:haml-rails) >= 0.8.2
BuildRequires:  rubygem(%{rb_default_ruby_abi}:hashie) >= 3.4
BuildRequires:  rubygem(%{rb_default_ruby_abi}:js-routes:1)
BuildRequires:  rubygem(%{rb_default_ruby_abi}:kramdown:1) >= 1.3
BuildRequires:  rubygem(%{rb_default_ruby_abi}:mail) >= 2.6
BuildRequires:  rubygem(%{rb_default_ruby_abi}:mime-types) < 3
BuildRequires:  rubygem(%{rb_default_ruby_abi}:mime-types) >= 2.5
BuildRequires:  rubygem(%{rb_default_ruby_abi}:minitest) >= 5.6
BuildRequires:  rubygem(%{rb_default_ruby_abi}:puma:2) >= 2.11
BuildRequires:  rubygem(%{rb_default_ruby_abi}:rails:4.2)
BuildRequires:  rubygem(%{rb_default_ruby_abi}:ruby_parser) >= 3.6.6
BuildRequires:  rubygem(%{rb_default_ruby_abi}:sass) >= 3.4
BuildRequires:  rubygem(%{rb_default_ruby_abi}:sass-rails) >= 5.0.1
BuildRequires:  rubygem(%{rb_default_ruby_abi}:sexp_processor) >= 4.5.1
BuildRequires:  rubygem(%{rb_default_ruby_abi}:spring:1) >= 1.3
BuildRequires:  rubygem(%{rb_default_ruby_abi}:virtus)

%if 0%{?suse_version} <= 1310
BuildRequires:  rubygem(%{rb_default_ruby_abi}:rake:10.4)
%endif

BuildRequires:  rubygem(%{rb_default_ruby_abi}:sprockets) >= 3.0
BuildRequires:  rubygem(%{rb_default_ruby_abi}:thor) >= 0.19
BuildRequires:  rubygem(%{rb_default_ruby_abi}:tilt:1.4)
BuildRequires:  rubygem(%{rb_default_ruby_abi}:uglifier)
BuildRequires:  rubygem(%{rb_default_ruby_abi}:web-console:2) >= 2.1

%if 0%{?bundle_gems}
%else
# SLES bundles all this stuff at build time, other distros just
# use runtime dependencies.
Requires:       rubygem(%{rb_default_ruby_abi}:fast_gettext) >= 0.9.2
Requires:       rubygem(%{rb_default_ruby_abi}:gettext_i18n_rails:1) >= 1.2
Requires:       rubygem(%{rb_default_ruby_abi}:gettext_i18n_rails_js) >= 1.0
Requires:       rubygem(%{rb_default_ruby_abi}:haml-rails) >= 0.8.2
Requires:       rubygem(%{rb_default_ruby_abi}:hashie) >= 3.4
Requires:       rubygem(%{rb_default_ruby_abi}:js-routes:1)
Requires:       rubygem(%{rb_default_ruby_abi}:kramdown:1) >= 1.3
Requires:       rubygem(%{rb_default_ruby_abi}:puma:2) >= 2.11
Requires:       rubygem(%{rb_default_ruby_abi}:rails:4.2)
Requires:       rubygem(%{rb_default_ruby_abi}:sass-rails:5.0) >= 5.0.1
Requires:       rubygem(%{rb_default_ruby_abi}:sass:3.4)
Requires:       rubygem(%{rb_default_ruby_abi}:sexp_processor) >= 4.5.1
Requires:       rubygem(%{rb_default_ruby_abi}:sprockets) >= 3.0
Requires:       rubygem(%{rb_default_ruby_abi}:tilt:1.4)
Requires:       rubygem(%{rb_default_ruby_abi}:virtus:1.0)

%if 0%{?suse_version} <= 1310
Requires:       rubygem(%{rb_default_ruby_abi}:rake:10.4)
%endif

%endif

BuildRequires:  %{rubydevel >= 1.8.7}
BuildRequires:  git
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel >= 2.6.21
BuildRequires:  libxslt-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel

%description
A web-based GUI for managing and monitoring the Pacemaker
High-Availability cluster resource manager.

# DOCS: This is the second section in the spec file. It is used to get the sources ready to build.
%prep
# DOCS: It simply unpacks the sources and cd's into the source directory
%setup
# DOCS: There aren't really any macros for this section. You should just put any commands here that you would need to use to build the software once you had untarred the source, patched it, and cd'ed into the directory. This is just another set of commands passed to sh, so any legal sh commands can go here (including comments).
%build
export NOKOGIRI_USE_SYSTEM_LIBRARIES=1
CFLAGS="${CFLAGS} ${RPM_OPT_FLAGS}"
export CFLAGS
make WWW_BASE=%{www_base} INIT_STYLE=%{init_style} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} BUNDLE_GEMS=%{expand:%{?bundle_gems:true}%{!?bundle_gems:false}} RUBY_ABI=%{rb_ver}


# There aren't really any macros here, either. You basically just want to put whatever commands here that are necessary to install. If you have make install available to you in the package you are building, put that here.
%install
make WWW_BASE=%{www_base} INIT_STYLE=%{init_style} DESTDIR=%{buildroot} BUNDLE_GEMS=%{expand:%{?bundle_gems:true}%{!?bundle_gems:false}} install
# copy of GPL
cp COPYING %{buildroot}%{www_base}/hawk/
%if 0%{?bundle_gems}
# get rid of gem sample and test cruft
rm -rf %{buildroot}%{www_base}/hawk/vendor/bundle/ruby/*/gems/*/doc
rm -rf %{buildroot}%{www_base}/hawk/vendor/bundle/ruby/*/gems/*/examples
rm -rf %{buildroot}%{www_base}/hawk/vendor/bundle/ruby/*/gems/*/samples
rm -rf %{buildroot}%{www_base}/hawk/vendor/bundle/ruby/*/gems/*/test
rm -rf %{buildroot}%{www_base}/hawk/vendor/bundle/ruby/*/gems/*/ports
rm -rf %{buildroot}%{www_base}/hawk/vendor/bundle/ruby/*/gems/*/ext
%endif
%if 0%{?suse_version}

# Hack so missing links to docs don't kill the build
mkdir -p %{buildroot}/usr/share/doc/manual/sle-ha-geo-quick_en-pdf
mkdir -p %{buildroot}/usr/share/doc/manual/sle-ha-guide_en-pdf
mkdir -p %{buildroot}/usr/share/doc/manual/sle-ha-manuals_en
mkdir -p %{buildroot}/usr/share/doc/manual/sle-ha-geo-manuals_en
mkdir -p %{buildroot}/usr/share/doc/manual/sle-ha-nfs-quick_en-pdf

# mark .mo files as such (works on SUSE but not FC12, as the latter wants directory to
# be "share/locale", not just "locale", and it also doesn't support appending to %%{name}.lang)
%find_lang hawk hawk.lang
# don't ship .po files (find_lang only grabs the mos, and we don't need the pos anyway)
rm %{buildroot}%{www_base}/hawk/locale/*/hawk.po
rm %{buildroot}%{www_base}/hawk/locale/*/hawk.po.time_stamp
rm %{buildroot}%{www_base}/hawk/locale/*/hawk.edit.po
# hard link duplicate files
%fdupes %{buildroot}
%else
# Need file to exist else %%files fails later
touch hawk.lang
%endif
# more cruft to clean up (WTF?)
rm -f %{buildroot}%{www_base}/hawk/log/*
# likewise .git special files
find %{buildroot}%{www_base}/hawk -type f -name '.git*' -print0 | xargs --no-run-if-empty -0 rm
%if 0%{?suse_version}
%{__ln_s} -f %{_sbindir}/service %{buildroot}%{_sbindir}/rchawk
%endif

install -p -d -m 755 %{buildroot}%{_sysconfdir}/hawk

%clean
rm -rf %{buildroot}

%if 0%{?suse_version}
# TODO(must): Determine sensible non-SUSE versions of these,
# in particular restart_on_update and stop_on_removal.

%verifyscript
%verify_permissions -e %{_sbindir}/hawk_chkpwd
%verify_permissions -e %{_sbindir}/hawk_invoke

%pre
%service_add_pre hawk.service

%post
%set_permissions %{_sbindir}/hawk_chkpwd
%set_permissions %{_sbindir}/hawk_invoke
%service_add_post hawk.service

%preun
%service_del_preun hawk.service

%postun
%service_del_postun hawk.service

%endif

%files -f hawk.lang
%defattr(644,root,root,755)
%attr(4750, root, %{gname})%{_sbindir}/hawk_chkpwd
%attr(4750, root, %{gname})%{_sbindir}/hawk_invoke
%attr(0755, root, root) %{_sbindir}/hawk_monitor
%dir %{www_base}/hawk
%{www_base}/hawk/app
%{www_base}/hawk/config
%{www_base}/hawk/lib
%dir %{www_base}/hawk/bin
%attr(0755, root, root)%{www_base}/hawk/bin/rake
%attr(0755, root, root)%{www_base}/hawk/bin/rails
%exclude %{www_base}/hawk/bin/hawk
%attr(0755, root, root)%{www_base}/hawk/bin/generate-ssl-cert
%attr(0755, root, root)%{www_base}/hawk/bin/bundle
%attr(0750, %{uname},%{gname})%{_sysconfdir}/hawk
%attr(0750, %{uname},%{gname})%{www_base}/hawk/log
%dir %attr(0750, %{uname},%{gname})%{www_base}/hawk/tmp
%attr(-, %{uname},%{gname})%{www_base}/hawk/tmp/cache
%attr(-, %{uname},%{gname})%{www_base}/hawk/tmp/explorer
%attr(-, %{uname},%{gname})%{www_base}/hawk/tmp/home
%attr(-, %{uname},%{gname})%{www_base}/hawk/tmp/pids
%attr(-, %{uname},%{gname})%{www_base}/hawk/tmp/sessions
%attr(-, %{uname},%{gname})%{www_base}/hawk/tmp/sockets
%exclude %{www_base}/hawk/tmp/session_secret
%{www_base}/hawk/locale/hawk.pot
%if 0%{?bundle_gems}
%{www_base}/hawk/.bundle
%endif
%{www_base}/hawk/public
%{www_base}/hawk/Rakefile
%if 0%{?bundle_gems}
%{www_base}/hawk/Gemfile
%{www_base}/hawk/Gemfile.lock
%else
%exclude %{www_base}/hawk/Gemfile
%exclude %{www_base}/hawk/Gemfile.lock
%endif
%{www_base}/hawk/COPYING
%{www_base}/hawk/config.ru
%{www_base}/hawk/test
%if 0%{?suse_version}
# itemizing content in %%{www_base}/hawk/locale to avoid
# duplicate files that would otherwise be the result of including hawk.lang
%dir %{www_base}/hawk/locale
%dir %{www_base}/hawk/locale/*
%dir %{www_base}/hawk/locale/*/*
%else
%{www_base}/hawk/locale
%endif

# Not doing this itemization for %%lang files in vendor, it's frightfully
# hideous, so we're going to live with a handful of file-not-in-%%lang rpmlint
# warnings for bundled gems.
%{www_base}/hawk/vendor

%if 0%{?bundle_gems}
%attr(0755, root, root) %{www_base}/hawk/vendor/bundle/ruby/*/bin/puma
%attr(0755, root, root) %{www_base}/hawk/vendor/bundle/ruby/*/bin/pumactl
%endif

%{_unitdir}/hawk.service
%if 0%{?suse_version}
%attr(-,root,root) %{_sbindir}/rchawk
%endif

%changelog
