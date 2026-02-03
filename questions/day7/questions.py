# 1.
for i in range(2, 100,2):
    print(i ,end=" ")
print("\n")

# 2.
a,b =0,1
print("Fibonacci series up to 10:")
while(True):
    print(a ,end=" ")
    a,b = b, a+b
    if a > 10:
        break
    
#3.
squares = [i**2 for i in range(1, 10)]
print("\nSquares from 1 to 9:", squares)

#4.
elements = [2,3,4,3,4,2,44,43,2,8,67,45,3,5,543,89,355,333]
print(max(elements))

#5.
elements = [2,3,4,3,4,2,44,43,2,8,67,45,3,5,543,89,355,333]
max_element=0
secondmax=0
for i in elements:
    if i>max_element:
        secondmax = max_element
        max_element = i
    elif i>secondmax and i!=max_element:
        secondmax = i
print("Second largest element is:", secondmax)

#6.
keys = ['a', 'b', 'c', 'd']
values = [1, 2, 3, 4]
my_dict = zip(keys, values)
result_dict = dict(my_dict)
print("Resulting dictionary:", result_dict)

#7.
list1 = [1, 2, 3, 4, 5]
list2= [2,4,7,5,9,0]
common_elements = set(list1).intersection(set(list2))
print("Common elements:", common_elements)

#8.
phonebpook = {'mohan': '1234', 'shyam': '5678', 'ram': '91011', 'hari': '1213'}
def search_contact(name):
    return phonebpook.get(name, "Contact not found")
def add_contact(name, number):
    if not number.isdigit():
        print("Invalid number format")
        return
    elif name in phonebpook:
        print("Contact already exists")
        return
    elif not name or not number:
        print("Name and number cannot be empty")
        return
    phonebpook[name] = number
def delete_contact(name):
    if name in phonebpook:
        del phonebpook[name]   
    else:
        print("Contact not found")     
def update_contact(name, number):
    if not number.isdigit():
        print("Invalid number format")
        return
    if name in phonebpook:
        phonebpook[name] = number 
    else:
        print("Contact not found")           
    

#9
def is_valid():
    s = "()[]{}"
    stack=[]
    mapping={')':'(', '}':'{', ']':'['}
    for char in s:
        if char in mapping:
            top=stack.pop() if stack else ''
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack
print(is_valid())


#10.
group_anagrams = ["eat", "tea", "tan", "ate", "nat", "bat"]
anagram_dict = {}
for word in group_anagrams:
    sorted_word = ''.join(sorted(word))
    if sorted_word in anagram_dict:
        anagram_dict[sorted_word].append(word)
    else:
        anagram_dict[sorted_word] = [word]
print("Grouped anagrams:", list(anagram_dict.values()))        
