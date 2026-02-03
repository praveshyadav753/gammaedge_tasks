list =[8,5,4,53]
print(list)
# del list
# l= list(range(10))
# print(l)

import builtins
l= builtins.list(range(10))
print(l)
# print(dir()) #list all the namespace name(keys)
print(globals(),end='\n\n') #list all the namespace globally in dict
# print(locals())  #list all the namespace locally in form of dic 

def func(x, y):
    message = "Hello!"
    print(locals())
func(3,5)    

