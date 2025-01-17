Name:		btanks
Version:	0.9.8083
Release:	4
Summary:	Funny battle on your desk
Group:		Games/Arcade
# Libraries clunk, mrt and sdlx are under LGPLv2+, all other sources are GPLv2+
License:	GPLv2+ with exceptions and LGPLv2+
URL:		https://btanks.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Remove RPath from binaries
Patch0:		btanks-remove-rpath.patch
# Disable video previews of map levels (we don't distribute video anyway)
Patch1:		btanks-disable-smpeg.patch
# Avoid problem with lib checks using c++ instead of c.
Patch2:		btanks-libcheck.patch
# Don't override Fedora's options
Patch3:		btanks-excessopts.patch
# gcc is now more picky about casting
Patch4:		btanks-gcc.patch
# bted doesn't explicitly link to clunl
Patch5:		btanks-dso.patch
Patch6:		btanks-gcc47.patch

Requires:	%{name}-data = %{version}-%{release}
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	lua-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	scons
BuildRequires:	zip
BuildRequires:	dos2unix
# Disabled video previews of map levels
BuildRequires:	smpeg-devel

%description
Battle Tanks is a funny battle on your desk, where you can choose one of three
vehicles and eliminate your enemy using the whole arsenal of weapons. has
original cartoon-like graphics and cool music, it is fun and dynamic, it has
several network modes for deathmatch and cooperative.
What else is needed to have fun with your friends?

And all is packed and ready for you in Battle Tanks.

%package	data
Summary:	Data files for %{name}
Group:		Games/Arcade
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	data
The %{name}-data package contains data files that are needed for
running %{name}.

%prep
%setup -q
%patch0 -p0 -b .remove-rpath
%patch1 -p0 -b .disable-smpeg
%patch2 -p0 -b .libcheck
%patch3 -p0 -b .excessopts
%patch4 -p0 -b .gcc
%patch5 -p0 -b .dso
%patch6 -p0 -b .gcc4.7
dos2unix -k *.txt ChangeLog *.url LICENSE LICENSE.EXCEPTION

iconv -f latin1 -t utf-8 LICENSE.EXCEPTION > LICENSE.EXCEPTION.new
touch -r LICENSE.EXCEPTION{,.new}
mv -f LICENSE.EXCEPTION{.new,}

iconv -f latin1 -t utf-8 README-fr.txt > README-fr.txt.new
touch -r README-fr.txt{,.new}
mv -f README-fr.txt{.new,}

iconv -f cp1251 -t utf-8 README-ru.txt > README-ru.txt.new
touch -r README-ru.txt{,.new}
mv -f README-ru.txt{.new,}


%build
# flags need to be passed via environment or they get treated as a single
# word rather than as multiple arguments. CXXFLAGS is only needed if
# there are c++ only flags that need to get added.
export CFLAGS="%{optflags}"; \
        scons \
        prefix=%{_prefix} \
        lib_dir=%{_libdir} \
        plugins_dir=%{_libdir}/%{name} \
        resources_dir=%{_gamesdatadir}/%{name} \
        mode=release \
        enable_lua=true

%install
# binaries
install -dm 755 %{buildroot}%{_gamesbindir}
install -m 755 build/release/engine/%{name} %{buildroot}%{_gamesbindir}
install -m 755 build/release/editor/bted %{buildroot}%{_gamesbindir}

# libs
install -dm 755 %{buildroot}%{_libdir}/%{name}
install -m 755 build/release/engine/libbtanks_engine.so %{buildroot}%{_libdir}
install -m 755 build/release/mrt/libmrt.so %{buildroot}%{_libdir}
install -m 755 build/release/sdlx/libsdlx.so %{buildroot}%{_libdir}
install -m 755 build/release/clunk/libclunk.so %{buildroot}%{_libdir}

# plugins
install -m 755 build/release/objects/libbt_objects.so %{buildroot}%{_libdir}/%{name}

# data-files (see pack-resources.sh)
install -dm 755 %{buildroot}%{_gamesdatadir}/%{name}
install -dm 755 %{buildroot}%{_gamesdatadir}/%{name}/data
pushd data
find . \( -wholename \*.svn\* -or -name \*.wav \) -exec rm -rf {} \;
cp -pR * %{buildroot}%{_gamesdatadir}/%{name}/data
#zip -q -0 -r ../resources.dat * -x \*.svn\* -x \*.wav
popd
#install -m 644 resources.dat %{buildroot}%{_datadir}/%{name}

# icon
install -dm 755 %{buildroot}%{_datadir}/pixmaps
install -D data/tiles/icon.png %{buildroot}%{_iconsdir}/%{name}.png

# menu-entries
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Battle Tanks
Comment=Battle Tanks is a funny battle on your desk
Comment[ru]=Battle Tanks — это веселая маленькая война на столе
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-bted.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Battle Tanks map editor
Name[ru]=Battle Tanks — редактор карт
Comment=Battle Tanks map editor
Comment[ru]=Редактор карт для Battle Tanks
Exec=%{_gamesbindir}/bted
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;
EOF

%files
%doc README-{editor,en,fr,ru}.txt ChangeLog *.url LICENSE LICENSE.EXCEPTION
%{_gamesbindir}/%{name}
%{_gamesbindir}/bted
%{_libdir}/*.so
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_iconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/applications/mandriva-bted.desktop

%files data
%defattr(-,root,root,-)
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/data


%changelog
* Mon Nov 28 2011 Andrey Bondrov <abondrov@mandriva.org> 0.9.8083-1mdv2011.0
+ Revision: 734933
- imported package btanks

