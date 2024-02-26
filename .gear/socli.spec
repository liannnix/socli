%define _unpackaged_files_terminate_build 1
%define pypi_name socli

%def_without check

Name:    %pypi_name
Version: 7.3
Release: alt1

Summary: Stack overflow command line interface
License: BSD-3-Clause
Group:   Other
URL:     https://pypi.org/project/%pypi_name
VCS:     https://github.com/gautamkrishnar/%pypi_name

BuildRequires(pre): rpm-build-pyproject
# Sphinx documentation
#BuildRequires: python3-module-sphinx

%pyproject_runtimedeps_metadata
%add_pyproject_deps_build_filter pytest-runner
%pyproject_builddeps_build

%if_with check
%pyproject_builddeps_metadata
#%%pyproject_builddeps_metadata_extra test
%pyproject_builddeps_check
%endif

#BuildRequires: python3-devel python3-module-setuptools python3-module-wheel

#Provides: %pypi_name = %EVR
#%%py3_provides %pypi_name

BuildArch: noarch

Source:  %name-%version.tar
Source1: %pyproject_deps_config_name

#Patch: %pypi_name-%version-alt.patch

%description
Stack Overflow command line written in python. Using SoCLI you can
search and browse Stack Overflow without leaving the terminal.

%package -n python3-module-%pypi_name
Summary: Python3 module for Stack overflow command line interface
Group:   Development/Python3
BuildArch: noarch

%description -n python3-module-%pypi_name
Python3 module for Stack Overflow command line written in python. Using SoCLI you can
search and browse Stack Overflow without leaving the terminal.

%prep
%setup -n %name-%version
#%%patch -p1
# hack for setuptools_scm
#%%pyproject_scm_init
%pyproject_deps_resync_build
%pyproject_deps_resync_metadata
# tox testing deps hack
#%%if_with check
#%%pyproject_deps_resync_check_tox tox.ini testenv
#%%endif

%build
%pyproject_build

# Sphinx documentation
#%%make -C docs html SPHINXBUILD=sphinx-build-3

%install
%pyproject_install
mkdir -p %buildroot%_man1dir
mv %buildroot/usr/man/man1/socli.1 %buildroot%_man1dir/%pypi_name.1

%check
#%%tox_create_default_config
%tox_check_pyproject
#%%pyproject_run_pytest -ra tests

%files
%_bindir/%pypi_name
%_man1dir/%pypi_name.*

%files -n python3-module-%pypi_name
%doc *.md *.rst
%python3_sitelibdir/%pypi_name/
%python3_sitelibdir/%{pyproject_distinfo %pypi_name}

%changelog
* Mon Feb 26 2024 Andrey Limachko <liannnix@altlinux.org> 7.3-alt1
- initial build
