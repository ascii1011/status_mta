
#status_mta

1. Note: create project folder and "$ cd project_folder"
2. "$ virtualenv env"
3. "$ source env/bin/activate"
4. "$ git clone git@github.com:ascii1011/status_mta.git"
5. "$ cd status_mta/"
6. "$ pip install -r requirements.txt"
7. "$ cd mta/"
8. "$ ./manage.py collectstatic"
9. "$ ./manage.py migrate"
10. "$ ./manage.py syncdb  #create an admin"
11. "$ ./manage.py runserver <ip_address>:<port>"