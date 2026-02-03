from logging import exception
from math import pi
# class student:
#     count=0
#     def __init__(self,name,id):
#         self.name = name
#         self.id=id
#         student.count += 1
#
#     @classmethod
#     def counts(cls):
#         print(cls.count)

#
#
# s1= student("rahul",1)
# s2 = student("shyam",2)
# s3 = student('mohit',7)
#
# student.counts()


class circle:
    radius= 0
    def __init__(self):
        pass

    @property
    def radiuss(self):
        return self.radius

    @radiuss.setter
    def radiuss(self,radius):
        self.radius = radius

    def cal_area(self):
        area = pi * pow(self.radius,2)
        return area

    def circumstance(self):
        circum= 2*pi*self.radius
        return circum
c1 = circle()
c1.radiuss = 5
print(c1)
print(c1.cal_area())



ValueError, TypeError, FileNotFoundError, ZeroDivisionError
try:
    with open('hrml.pdf','r') as f:
        readline(f)
except FileNotFoundError as e:
    print(e)

else:
    print("successfull")

try:
    "string"+1
except TypeError as e:
      print(e)
except ZeroDivisionError:
    print(e)
else:
    print("run")




# ................
class animal:
    def sound():
      pass
class dog(animal):
    def sound():
        print("bhaau")
class cat(animal):
    def sound(self):
        print("meooww")

d1 = dog.sound()
c1 = cat.sound()

