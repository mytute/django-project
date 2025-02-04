# Django Quick Practice On LOCAL 

```bash 
$ mkdir django-mysql && cd django-mysql
$ pip install virtualenv
$ virtualenv --version
$ virtualenv venv
$ source venv/bin/activate
$ pip list  
```

install the Python 3 and MySQL development headers and librarie    
[doc](https://pypi.org/project/mysqlclient/)  
```bash
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config # Debian / Ubuntu
$ sudo yum install python3-devel mysql-devel pkgconfig # Red Hat / CentOS
```

install django and mysql client for virtual env   
```bash
$ pip install django mysqlclient
```


