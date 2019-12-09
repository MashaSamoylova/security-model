
import pymysql
import random
import string
import hashlib

from pymysql.cursors import DictCursor


CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits

DELIVERY_BOY = ['Antoniy', 'Mashka', 'Natashka']
TRANSPORT = ['car', 'bicycle', 'no']
PRODUCT = ['pizza1', 'pizza2', 'pizza2']
CLIENTS = ['user1', 'user2', 'user3', 'user4', 'user5']
PRODUCT_DESCRIPTION = ['Сочная пицца', 'Сырная пицца', 'Ароматная пицца']
ADMIN = ['Admin1', 'Admin2']
ADDRESS = ['Tomsk', 'SEVERSK']

def generate_name():
    size = random.randint(8, 12)
    return ''.join(random.choice(CHARS) for x in range(size))


def hash(password):
    return hashlib.sha256(password.encode()).hexdigest()



def fill_database():
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='shop',
        charset='utf8mb4',
        cursorclass=DictCursor
    )

    for i in range(len(CLIENTS)):
        login = CLIENTS[i]
        password = hash(CLIENTS[i])
        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO clients 
                (login, password)
                VALUES
                ("{login}", "{password}")"""
            cursor.execute(query)
            connection.commit()
    
    for i in range(len(ADMIN)):
        login = ADMIN[i]
        password = hash(ADMIN[i])
        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO admins 
                (login, password)
                VALUES
                ("{login}", "{password}")"""
            cursor.execute(query)
            connection.commit()

    for i in range(len(DELIVERY_BOY)):
        login = DELIVERY_BOY[i]
        password = hash(DELIVERY_BOY[i])
        transport = TRANSPORT[random.randint(0,2)]
        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO delivery_boys 
                (login, password, transport)
                VALUES
                ("{login}", "{password}", "{transport}")"""
            cursor.execute(query)
            connection.commit()
    
    for i in range(10):
        title = PRODUCT[random.randint(0, 2)]
        description = PRODUCT_DESCRIPTION[random.randint(0,2)]
        price = random.randint(100, 1000)
        edited_by_login = ADMIN[random.randint(0,1)]

        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO products 
                (title, description, price, edited_by_login)
                VALUES
                ("{title}", "{description}", {price}, "{edited_by_login}" )"""
            cursor.execute(query)
            connection.commit()
    
    for i in range(10):
        delivery_boy_login = DELIVERY_BOY[random.randint(0,2)]
        payment_by_login = CLIENTS[random.randint(0, len(CLIENTS)-1)]
        client_name = generate_name()
        delivery_address = ADDRESS[random.randint(0,1)]
        mobile_number = random.randint(10000000000, 99999999999)

        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO orders 
                (
                    delivery_boy_login, 
                    payment_by_login, 
                    client_name, 
                    delivery_address, 
                    mobile_number, 
                    date_time
                )
                VALUES
                (
                    "{delivery_boy_login}", 
                    "{payment_by_login}", 
                    "{client_name}", "{delivery_address}",
                    "{mobile_number}",
                    NOW()
                )
                """
            print(query)
            cursor.execute(query)
            connection.commit()
    

    for i in range(10):
        client_login = random.choice(CLIENTS)
        text = generate_name()

        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO rewiews 
                (
                    client_login, 
                    date_time, 
                    text
                )
                VALUES
                (
                    "{client_login}", 
                    NOW(), 
                    "{text}"
                )
                """
            print(query)
            cursor.execute(query)
            connection.commit()
    

    for i in range(10):
        order_id = random.randint(2, 11)
        product_id = random.randint(1,10)
        quantity = random.randint(1,100)

        with connection.cursor() as cursor:
                query = f"""
                    INSERT INTO contain 
                    (
                        order_id, 
                        product_id, 
                        quantity
                    )
                    VALUES
                    (
                        {order_id}, 
                        {product_id}, 
                        {quantity}
                    )
                    """
                print(query)
                cursor.execute(query)
                connection.commit()
    
    for i in range(10):
        client_login = random.choice(CLIENTS)
        product_id = random.randint(1,10)
        with connection.cursor() as cursor:
                query = f"""
                    INSERT INTO browse 
                    (
                        client_login, 
                        product_id
                    )
                    VALUES
                    (
                        "{client_login}", 
                        {product_id}
                    )
                    """
                print(query)
                cursor.execute(query)
                connection.commit()



    


        
    





if __name__=="__main__":
    fill_database()