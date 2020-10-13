# import os,subprocess
import csv
from ecommerce.models import Product
from django.core.files import File
from django.db import models
# # print(Product.objects.all()[0].name)

with open('test.csv',encoding='utf8',newline='') as csvfile:
    spamreader=csv.reader(csvfile,delimiter=',')
    for i,row in enumerate(spamreader):
        # print(row)
        if i==0:
            continue
        try:
            product1=Product(category=row[0],sub_category=row[1],name=row[2],regular_price=row[3],discounted_price=row[4])
            name=row[2]
            name=name.replace(":","")
            name=name.replace("*","")
            name=name.replace(".","")
            name=name.replace("\"","")
            name=name.replace("/","")
            name=name.replace("\\","")
            name=name.replace("[","")
            name=name.replace("]","")
            name=name.replace(";","")
            name=name.replace("|","")
            name=name.replace(",","")
            image=models.ImageField()
            product1.image.save(f"{name}.jpg", File(open("C:\\Users\\hp\\projectsdjango\\flashkart_clean\\test_images\\{}.png".format(name), 'rb')))
        except FileNotFoundError:
            print(product1.name)
        
print(Product.objects.all()[0].name)
        # for i in Product.objects.all():
        #     print(i.image)
        # if len(row)>1:
            # print(row[2],row)
            # list1.append(row[2])
# print(list1)
# print("a")



# cmd automate with it     ####################################################################3

# abs_path=os.path.abspath('manage.py')
# print(abs_path) #will get full path along with manage.py
# print(os.path.dirname(abs_path)) #will remove manage.py 

# print(os.path.dirname(abs_path)+"\\ecommerce\\static\\")
# print(os.path.join(os.path.dirname(abs_path),"ecommerce","static")) # will add values to path
# for i in range(9):
#     os.system('cmd /k "pwd"')
# for i in range(9):
# subprocess.run('ls')
# subprocess.run('python manage.py shell')
# subprocess.run('from ecommerce.models import Product')
# subprocess.run('from django.core.files import File')
# subprocess.run('Product.objects.all()')
# subprocess.run('exit()')