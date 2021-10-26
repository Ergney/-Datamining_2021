import pymysql
from config import host, user, password, bd_name
import parce_data

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=bd_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connection successful")

    try:
        # cursor = connection.cursor()
        with connection.cursor() as cursor:
            create_table_query = "CREATE TABLE IF NOT EXISTS `best films`" \
                                 "(" \
                                 "id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                 "site_id int UNSIGNED," \
                                 "posterlink VARCHAR(300)," \
                                 "rus_title varchar(300)," \
                                 "original_title varchar(300)," \
                                 "hasTrailer bit," \
                                 "year int UNSIGNED," \
                                 "rating float(10) UNSIGNED," \
                                 "votes bigint UNSIGNED," \
                                 "availability bit" \
                                 ");"
            cursor.execute(create_table_query)
            print("The table was created successfully")
        parcer = parce_data.Parce_kinopoisk()
        data = parcer.get_data()
        with connection.cursor() as cursor:
            for page in data:
                insert_query = "INSERT INTO `best films` (`site_id`,`posterlink`,`rus_title`,`original_title`,`hasTrailer`,`year`,`rating`,`votes`,`availability`)" \
                               "VALUES" \
                               f"{page};"
                cursor.execute(insert_query)
                connection.commit()
    finally:
        connection.close()

except Exception as ex:
    print('Connection error')
    print(ex)