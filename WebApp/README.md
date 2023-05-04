This is Flask web application that takes the image of a mushroom to predict whether or not it is poisonous
It uses MySQL as the database and Redis for caching, then you should have these two on your system.
The SQL scripts are uploaded so you can use them. If you change the names or fields, be careful to apply those modifications to the code as well!
The database connection secrets are stored in a .env file not uploaded here for privacy, you can follow the env-template file to create your own version of the .env file.
installation of a virtual env is highly recommended
install the requirements.txt libraries and packages
run python app.py (don't forget to activate your virtual env if installed)


References and projects used to develop this app:
-------------------------------------------------

1.https://github.com/FunCodingPanda/Mushroom_Image_Classification/blob/master/Mushroom_Capstone.ipynb  (ML Model for Mushroom Classification)

2.https://github.com/mvmanh/dog-cat-classification (Flask Cat and Dog Image Classification)

3.https://github.com/matteozw/python_flask_mysqldb (User Authentication and Session Management)