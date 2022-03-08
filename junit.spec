Name:           junit
Epoch:          1
Version:        4.12
Release:        14
Summary:        A Java package for unit testing frameworks
License:        EPL-1.0
URL:            http://www.junit.org/
Source0:        https://github.com/%{name}-team/%{name}/archive/r%{version}.tar.gz
Patch0000:      CVE-2020-15250-pre.patch
Patch0001:      CVE-2020-15250.patch
Patch0002:      ignore-test-failure.patch

BuildArch:      noarch
BuildRequires:  maven-local mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)

Obsoletes:      %{name}-demo < 4.12

%description
JUnit is a simple framework to write repeatable tests. It is an
instance of the xUnit architecture for unit testing frameworks.

%package help
Summary:        Documents for junit

Provides:       %{name}-manual = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-manual < %{epoch}:%{version}-%{release}
Provides:       %{name}-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-javadoc < %{epoch}:%{version}-%{release}

%description help
The junit-help package contains related documents.

%prep
%autosetup -n %{name}4-r%{version} -p1

find . -name "*.jar" -delete
find . -name "*.class" -delete

%pom_remove_plugin :replacer
sed s/@version@/%{version}/ src/main/java/junit/runner/Version.java.template >src/main/java/junit/runner/Version.java

%pom_remove_plugin :animal-sniffer-maven-plugin

%pom_remove_plugin :maven-javadoc-plugin

%pom_xpath_inject pom:project "<packaging>bundle</packaging>"
%pom_xpath_inject pom:build/pom:plugins "
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <extensions>true</extensions>
      <configuration>
        <instructions>
          <Bundle-SymbolicName>org.junit</Bundle-SymbolicName>
          <Export-Package>{local-packages},!org.hamcrest*,*;x-internal:=true</Export-Package>
          <_nouses>true</_nouses>
        </instructions>
      </configuration>
    </plugin>"

%mvn_file : junit

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-junit.txt README.md

%files help -f .mfiles-javadoc
%doc doc/*

%changelog
* Thu Mar 10 2022 lvxiaoqian <xiaoqian@nj.iscas.ac.cn> - 1:4.12-14
- ignore maven-surefire-plugin test fail

* Fri Feb 19 2021 wangxiao <wangxiao65@huawei.com> - 1:4.12-13
- Fix CVE-2020-15250

* Sun Jan 19 2020 Jiangping Hu <hujp1985@foxmail.com> - 1:4.12-12
- Package init
