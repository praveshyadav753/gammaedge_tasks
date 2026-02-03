
class overflowError(Exception):
    pass
class underflowError(Exception):
    pass
class stack:
    def __init__(self):
        self.list = []
        self.limit = 10

    def overflow(self):
        if len(self.list) > 10:
            raise OverflowError("stack is full, can't push item")
    def underflow(self):
        if len(self.list)<1:
            raise underflowError("Stack is empty")
    def push(self,number):
        try :
            self.overflow()
            self.list.append(number)
        except overflowError as e:
             print("overflow",e)
        else:
            print("inserted")
    def pop(self):
        try:
            self.underflow()
            print(self.list.pop())
        except underflowError as e:
            print(e)
        else:
            print("poped")



st = stack()
st.push(2)
st.push(4)
st.push(2)
st.push(5)
st.push(24)
st.push(2)
st.push(5)
st.push(7)
st.push(8)
st.push(1)
st.push(8)
st.push(89)
st.pop()

