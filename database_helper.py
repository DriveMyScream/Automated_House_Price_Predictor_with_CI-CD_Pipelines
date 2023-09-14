import mysql.connector

class DataBaseHelper:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host='127.0.0.1',
                                                      user='root',
                                                      password='admin',
                                                      database='home_prices')
            self.mycursor = self.connection.cursor()
        except Exception as e:
            print("Connection Error:", str(e))

    def insert_values(self, data):
        try:
            query = """
            INSERT INTO home_details
            (area, latitude, longitude, bedrooms, bathrooms, balcony, neworold, parking, furnished_status, lift, type_of_building, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Convert the list to a tuple before passing it as a parameter
            data_tuple = tuple(data)
            self.mycursor.execute(query, data_tuple)
            self.connection.commit()
        except Exception as e:
            print("Insert Error:", str(e))