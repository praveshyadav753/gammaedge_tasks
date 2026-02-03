# a,b =map(int, input("enter two number").split(' '))
# a = a+b
# b = a-b
# a = a-b
# print(f"after: a:{a},b:{b}")

# # --------------------------------------------------
# name,age =input().split(',')

# print(f"name:{name},age:{age}")
# # --------------------------------------------------
# number = int(input("number"))
# iseven = ""
# iseven = "even" if number%2==0 else "odd"
# print(iseven)
# ---------------------------------------------------------
# temperature_f= int(input("enter temperature in fer "))
# Incel = (temperature_f-32)*5/9
# print(f"fer:{Incel}")
# temperature_c=int(input("Enter temperature in cel"))
# indeg=(temperature_c*5/9)+32
# print(f"Degree:{indeg}")
# ---------------------------------------------------------------
# input_str = input("Enter string to check : ")
# input_str=input_str.lower()
# is_palindrome = False
# is_palindrome = input_str == input_str[::-1]
# print(is_palindrome)
# --------------------------------------------------------
# input_string = input("Enter string")
# frq ={}
# for i in input_string:
#         frq[i]= frq.get(i,0)+1
# for key,value in frq.items():
#         print(f"{key}:{value}")   

# -----------------------------------------------------
# age=23
# name="pravesh"

# print(f"name :{name},age:{age}")
# print("name : %s ,age: %i" %(name,age))
# print("name: {},age: {}".format(name,age))

# # --------------------------------------------------------
# year = int(input("Enter year"))
# isleap= False
# isleap = True if year%4==0 else False

# ----------------------------------------------
# input_str1 =input("sring 1:")
# input_str2 = input("string 2")

# input_str1 = sorted(input_str1)
# input_str2 = sorted(input_str2)

# is_anangram = True if input_str1 == input_str2 else False

# print(is_anangram)

# # ----------------------------------
print("select operation", end="\n")
print(".......................................")
choice= int(input("1. Addition \n 2. subtraction \n 3.division  \n 4. multiplication"))

def addition(*args):
    sum=0
    for i in args:
        print(i)
        sum =sum +i
    return sum   
def sutraction(*args):
    sub=args[0]
    for i in args[1:]:
        sub-=i
    return sub
def multiplication(*args):
    result = 0
    for i in args:
        result *=i
    return result
def division(*args):
    result=args[0]
    for i in args[1:]:
     result/=i
    return result 
    

    

if choice==1:
    args = [int(num) for num in input("numbers sep by space").split() if num.isdigit()]
    print(addition(*args))
elif choice==2:
    args = [int(num) for num in input("numbers sep by space").split() if num.isdigit()]
    print(sutraction(*args))
elif choice==3:
    args = [int(num) for num in input("numbers sep by space").split() if num.isdigit()]
    print(division(*args))
elif choice==4:
    args = [int(num) for num in input("numbers sep by space").split() if num.isdigit()]
    print(multiplication(*args))
else:
    print("invalid choice")      
   







