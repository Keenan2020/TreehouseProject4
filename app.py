import os
import csv
import datetime
from datetime import date
from collections import OrderedDict

from peewee import *
from peewee import DoesNotExist

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField() # primary_key=True is implied
    product_name = CharField(max_length=25, unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateField()

    class Meta:
        database = db


def add_data(**kwargs):
    # print(kwargs)
    try:
        kwargs['product_price'] = clean_price(kwargs['product_price'])
        kwargs['product_quantity'] = int(kwargs['product_quantity'])
        kwargs['date_updated'] = datetime.datetime.strptime(kwargs['date_updated'], '%m/%d/%Y')
        product = Product.get(**kwargs)
        if product:
            product.product_name = kwargs['product_name']
            product.product_price = kwargs['product_price']
            product.product_quantity = kwargs['product_quantity']
            product.date_updated = kwargs['date_updated']
            product.save()
    except DoesNotExist:
        print("DoesNotExist")
        Product.create(product_name = kwargs['product_name'],
            product_price = kwargs['product_price'],
            product_quantity = kwargs['product_quantity'],
            date_updated = kwargs['date_updated']).save()        


def csv_data():
    with open("inventory.csv") as csvfile:
        product_reader = csv.DictReader(csvfile, delimiter= ',')
        for row in product_reader:
            add_data(**row)
           


#Menu Functions            
def view_entry():
    '''View Single Products Inventory'''
    clear()
    select = int(input("What is the product ID: \n").strip())
    query = Product.select().where(Product.product_id == select)
    for row in query:
        print(f"The product is {row.product_name} \nThe Quantity is {row.product_quantity} \nThe Price is {convert_dollar(row.product_price)}")
        
    

def add_entry():
    '''Add A New Product '''
    p_name = input("What is the product name: ").strip()
    p_quantity = input("How many of the product is there: ").strip()
    p_price = input("What does the product cost: ").strip()
    now = datetime.datetime.now()
    p_date = now.strftime('%m/%d/%Y')
    
    add_data(product_name=p_name, product_quantity=p_quantity, product_price=p_price, date_updated=p_date)


def backup_data(): 
    '''Create Backup Of Inventory'''
    database_data = Product.select()
    with open("backup_file.csv", 'a') as csvfile:
        writer = csv.writer(csvfile)
        fieldnames = ['product_name','product_price','product_quantity','date_updated']
        header = csv.DictWriter(csvfile, fieldnames = fieldnames)
        header.writeheader()

        for row in database_data:
            writer.writerow([
                row.product_name,
                convert_dollar(row.product_price),
                row.product_quantity,
                row.date_updated
            ])
    print("***Data Saved!***")

#Menu
def menu_loop():
    choice = None   
    while choice != 'q':
        
        print("\nStore Inventory")
        print("=" * 15)
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        print("q) Quit\n")      

        choice = input("Action: ").lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


menu = OrderedDict([
    ('v', view_entry),
    ('a', add_entry),
    ('b', backup_data),
])


#Maintenance
def clean_price(dollars):
    return int(dollars.replace("$","").replace(".",""))

def convert_dollar(cent):
    return float(cent/100)  

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Start 
def initialize():
    db.connect()
    db.create_tables([Product], safe=True) 

if __name__ == '__main__':
    initialize()
    csv_data() 
    menu_loop()
    #view_entry()