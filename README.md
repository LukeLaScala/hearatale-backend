install mysql
install python3.5+

pip install flask
pip install flask-login
pip install flask-sqlalchemy
pip install flask-mysqldb

open mysql
create a user with ```create user hearatale@localhost;```
give privs to the table ```grant all privileges on hearatale.* to hearatale@localhost```

`python3.6` or whatever version of python you have

```
from hearatale import *
db.create_all() # this creates all the tables
```
