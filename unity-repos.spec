# Set this to 1 when in devel stage
# Set this back to 0 when at RC stage
%define am_i_cauldron 1

%if %{distro_arch} == "x86_64"
%global secondary_distarch i586
%endif

Name:     unity-repos
# When Cauldron becomes new release, Version must match new release
Version:  1
# During Cauldron devel, it should be 0.0.X
# During release candidate, it should be 0.1.X
# Before final release, bump to 1
Release:  %mkrel 0.0.1
Summary:  Unity package repositories
Group:    System/Packaging
License:  MIT

# Unity GPG key
Source0:  RPM-GPG-KEY-Unity

# Unity release repo config templates
Source1:  Unity-Linux-mageia.repo

Provides: unity-repos(%{version})
Provides: unity-repos(releasever) = %{version}
Requires: system-release(releasever) >= %{version}
Requires: unity-repos-pkgprefs = %{version}-%{release}
Requires: unity-repos-keys = %{version}-%{release}

# At RC stage, after switching off am_i_cauldron, add the appropriate Obsoletes
#Obsoletes: unity-repos-cauldron < VERSION-0.1

%description
Unity package repository files for DNF and PackageKit with GPG public keys


%package keys
Summary:  Unity repository GPG keys
Group:    System/Packaging
# GPG keys are architecture independent
BuildArch: noarch

%description keys
Unity GPG keys for validating packages from Unity repositories by
DNF and PackageKit.

%package pkgprefs
# (ngompa): See the following page on why this exists:
# https://fedoraproject.org/wiki/PackagingDrafts/ProvidesPreferences#Distribution_preference
Summary:  Unity repository package preferences
Group:    System/Packaging
# Preferences list is architecture independent
BuildArch: noarch

## Base packages

# webfetch
Suggests: curl

# webclient
Suggests: lynx

# bootloader
Suggests: grub2

# vim
Suggests: vim-minimal

# Always prefer perl-base over weird packages auto-providing same modules
Suggests: perl-base

# libGL.so.1 (also provided by proprietary drivers)
Suggests: libmesagl1
Suggests: lib64mesagl1

# Prefer openssl over libressl
Suggests: libopenssl1.0.0
Suggests: lib64openssl1.0.0

# Prefer openssh-askpass over openssh-askpass-gnome (for keychain)
Suggests: openssh-askpass

# Python 2.7
Suggests: python

# Initrd
Suggests: dracut

## Multimedia

# festival-voice
Suggests: festvox-kallpc16k

# gnome-speech-driver
Suggests: gnome-speech-driver-espeak

# esound
Suggests: pulseaudio-esound-compat

# gst-install-plugins-helper
Suggests: packagekit-gstreamer-plugin

# libbaconvideowidget.so.0 (totem backend)
Suggests: libbaconvideowidget-gstreamer0
Suggests: lib64baconvideowidget-gstreamer0

# phonon-backend: prefer phonon-vlc over phonon-gstreamer
Suggests: phonon-vlc

# phonon4qt5-backend: prefer phonon4qt5-vlc over phonon4qt5-gstreamer
Suggests: phonon4qt5-vlc

# mate backends
Suggests: matemixer-backend-pulse

# mate menu layout
Suggests: matemenu-unity-layout

## Devel

# xemacs-extras provides ctags, prefer simple ctags
Suggests: ctags

# prefer openssl-devel over libressl-devel
Suggests: libopenssl-devel
Suggests: lib64openssl-devel

# prefer gcc over gcc3.3
# (gcc-cpp and gcc-c++ are no more needed, but keeping just in case)
Suggests: gcc
Suggests: gcc-cpp
Suggests: gcc-c++
Suggests: libstdc++-devel

# prefer dnf-utils over urpmi-debuginfo-install
# (when using dnf, this is preferred, urpmi will prefer urpmi-debuginfo-install)
Suggests: dnf-utils

# prefer over lib(64)ossp_uuid packages
Suggests: libuuid-devel
Suggests: lib64uuid-devel

# prefer MIT krb5 over heimdal
Suggests: libkrb53-devel
Suggests: lib64krb53-devel

## Servers

# sendmail-command and mail-server
Suggests: postfix

# webserver
Suggests: apache

# nfs-server
Suggests: nfs-utils

# ftpserver
Suggests: proftpd

# postgresql
Suggests: libpq5
Suggests: lib64pq5

# syslog-daemon
Suggests: rsyslog

# vnc
Suggests: tigervnc

# x2goserver database backend
Suggests: x2goserver-sqlite

## Various
# sane (also provided by saned)
Suggests: sane-backends

# virtual-notification-daemon
Suggests: notification-daemon

# sgml-tools
# (the other choice is linuxdoc-tools which requires docbook-utils anyway)
Suggests: docbook-utils

# input method
Suggests: ibus
Suggests: pyzy-db-open-phrase
Suggests: ibus-ui-gtk3
# plasma-applet-kimpanel-backend: prefer plasma-applet-kimpanel-backend-ibus to plasma-applet-kimpanel-backend-scim
# Removed due to bug 8459
#Suggests: plasma-applet-kimpanel-backend-ibus 

# drupal database storage
Suggests: drupal-mysql

# polkit-agent
Suggests: mate-polkit

# java
Suggests: java-1.8.0-openjdk
Suggests: java-1.8.0-openjdk-devel

# java-plugin
Suggests: icedtea-web

# kde-display-management: prefer kscreen to krandr for mga4
Suggests: kscreen

# lightdm greeter
Suggests: lightdm-gtk3-greeter

# prefer netcat-traditional over netcat-openbsd since it is explicitly required by task-printing
# and the netcat packages are conflicting
Suggests: netcat-traditional

%description pkgprefs
This package supplies DNF and PackageKit with global
preferences for packages in which multiple options are possible.

%prep
# Nothing to prepare

%build
# Nothing to build

%install
# Install the GPG key
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install %{S:0} -pm 0644 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

# Install the repositories
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d

## Create the repositories for various sections
install %{S:1} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/unity-%{distro_arch}.repo

## Fill in the correct values for the installed repo files
sed -e "s/@DIST_ARCH@/%{distro_arch}/g" -i %{buildroot}%{_sysconfdir}/yum.repos.d/*%{distro_arch}*.repo

## For architectures with a secondary arch, we need to create repositories for them, too
%if %{defined secondary_distarch}
### Create the repositories for various sections, excluding sources (as they are identical to primary arch ones)
install %{S:1} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/unity-%{secondary_distarch}.repo

### Fill in the correct values for the installed repo files
sed -e "s/@DIST_ARCH@/%{secondary_distarch}/g" -i %{buildroot}%{_sysconfdir}/yum.repos.d/*%{secondary_distarch}*.repo

%endif


%check
%if %am_i_cauldron
case %release in 
    0.*) ;;
    *)
    echo "Cauldron distro should have this package with release < %{mkrel 1}"
    exit 1
    ;;
esac
%endif


%files
%dir %{_sysconfdir}/yum.repos.d
%config(noreplace) %{_sysconfdir}/yum.repos.d/unity*.repo

%files keys
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-Unity

%files pkgprefs
