CREATE DATABASE shop CHARACTER set utf8;

USE shop;

CREATE TABLE admins (
    login varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    PRIMARY KEY (login)
);

CREATE TABLE clients (
    login varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    PRIMARY KEY (login)
);

CREATE TABLE delivery_boys (
    login varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    transport varchar(100) NOT NULL,
    PRIMARY KEY (login)
);

CREATE TABLE products (
    id int AUTO_INCREMENT NOT NULL,
    title varchar(256) NOT NULL,
    description varchar(4096),
    price decimal(8, 2) NOT NULL,
    image blob,
    edited_by_login varchar(100) NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (edited_by_login)
        REFERENCES admins(login)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE orders (
    id int AUTO_INCREMENT NOT NULL,
    delivery_boy_login varchar(100) NOT NULL,
    payment_by_login varchar(100) NOT NULL,
    client_name varchar(100) NOT NULL,
    delivery_address varchar(255) NOT NULL,
    mobile_number char(12) NOT NULL,
    date_time datetime NOT NULL,
    payment_status boolean,
    delivery_status boolean,

    PRIMARY KEY (id),
    FOREIGN KEY (delivery_boy_login)
        REFERENCES delivery_boys(login)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
    
    FOREIGN KEY (payment_by_login)
        REFERENCES clients(login)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);


CREATE TABLE rewiews (
    id int AUTO_INCREMENT NOT NULL,
    client_login varchar(100) NOT NULL,
    date_time datetime NOT NULL,
    text varchar(4096) NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (client_login)
        REFERENCES clients(login)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE contain (
    id int AUTO_INCREMENT NOT NULL,
    order_id int NOT NULL,
    product_id int NOT NULL,
    quantity int NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (order_id) 
        REFERENCES  orders(id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
    FOREIGN KEY (product_id)
        REFERENCES products(id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE browse (
    id int AUTO_INCREMENT NOT NULL,
    client_login varchar(100) NOT NULL,
    product_id int NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (client_login)
        REFERENCES clients(login)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
    FOREIGN KEY (product_id)
        REFERENCES products(id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
