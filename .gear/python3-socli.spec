%define _unpackaged_files_terminate_build 1
%define pypi_name socli
#%define mod_name $module

%def_without check

Name:    python3-module-%pypi_name
Version: 7.3
Release: alt1

Summary: $summary
License: $license
Group:   Development/Python3
URL:     $url
#VCS:     $url

BuildRequires(pre): rpm-build-pyproject
# Sphinx documentation
#BuildRequires: python3-module-sphinx

%pyproject_runtimedeps_metadata
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

Source: %name-%version.tar
#Source1: %pyproject_deps_config_name

#Patch: %pypi_name-%version-alt.patch

%description
$description

#%package docs
#Summary: Documentation for %pypi_name
#Group: Development/Documentation
#BuildArch: noarch
#
#%description docs
#$description
#
#This package contains documentation for %pypi_name.

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

%check
#%%tox_create_default_config
%tox_check_pyproject
#%%pyproject_run_pytest -ra tests

%files
%doc *.md
%python3_sitelibdir/%pypi_name/
#%%python3_sitelibdir/%mod_name/
%python3_sitelibdir/%{pyproject_distinfo %pypi_name}

#%%files docs
#%%doc docs/_build/html/*
#%%doc examples

%changelog
* Wed Jan 17 2024 Aleksey Saprunov <sav@altlinux.org> 7.3-alt1
- initial build
