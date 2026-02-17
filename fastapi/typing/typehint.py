from typing import NewType,TypeAlias,Union


vector : TypeAlias = list[float]
print(type(vector))
UserId = NewType('UserId', int)
some_id = UserId(524313)
print(type(some_id))

def get_user_name(user_id: UserId,data=vector) -> str:
    print(f"UserId {user_id},data {data}")
    return str(user_id)


def get_data(user_id: UserId,id:Union[int,float] ) -> None:
    print(f"UserId {user_id},id {id}")

print(get_data(some_id,67))

user_a = get_user_name((42351),[2.4,"hello",23])
