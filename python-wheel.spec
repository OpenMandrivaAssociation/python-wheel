%bcond_without bootstrap

%define pypi_name wheel

%global python_wheelname %{pypi_name}-%{version}-py.py-none-any.whl
%global python_wheeldir %{_datadir}/python-wheels

Name:		python-%{pypi_name}
Version:	0.45.1
Release:	2
Summary:	A built-package format for Python
Group:		Development/Python
License:	MIT
URL:		https://bitbucket.org/pypa/wheel
Source0:	https://files.pythonhosted.org/packages/source/w/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(setuptools)

%if %{without bootstrap}
BuildRequires:	python-pip
%endif

%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

%package wheel
Summary:	The Python wheel module packaged as a wheel
Group:		Development/Python

%description wheel
A Python wheel of wheel to use with virtualenv.

%prep
export LC_ALL=C.utf-8
%autosetup -n %{pypi_name}-%{version}

%build
%py_build

%install
%py_install

mv %{buildroot}%{_bindir}/%{pypi_name}{,-%{python3_version}}
ln -s %{pypi_name}-%{python3_version} %{buildroot}%{_bindir}/%{pypi_name}-3
ln -s %{pypi_name}-3 %{buildroot}%{_bindir}/%{pypi_name}

%if %{without bootstrap}
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%py_build_wheel
mkdir -p %{buildroot}%{python_wheeldir}
install -p dist/%{python_wheelname} -t %{buildroot}%{python_wheeldir}
%endif

%if %{without bootstrap}
%endif

%files
%doc README.rst
%{_bindir}/%{pypi_name}
%{_bindir}/%{pypi_name}-3
%{_bindir}/%{pypi_name}-%{python_version}
%{python_sitelib}/%{pypi_name}*

%if %{without bootstrap}
%files wheel
%license LICENSE.txt
# we own the dir for simplicity
%dir %{python_wheeldir}/
%{python_wheeldir}/%{python_wheelname}
%endif
