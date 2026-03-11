import os

if os.getenv("DATABASE_URL"):
    import pymysql
    pymysql.install_as_MySQLdb()