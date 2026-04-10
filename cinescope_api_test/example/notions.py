from typing import Dict, Tuple, Set

def user_info() -> Dict[str, int]:
    return {"age": 25, "height": 180}
def get_coordinates() -> Tuple[float, float]:
    return (55.7558, 37.6173)  # Москва: широта, долгота
def unique_numbers(numbers: Set[int]) -> Set[int]:
    return set(numbers)
def func(numbers: list[int]) -> list[int]:
    return numbers

# Классы
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"

user = User("Алексей", 30)
print(user.greet())


# Optional
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None


# Union
def process_input(value: int | str) -> str:
    return f"Ты передал: {value}"

print(process_input(10))


# 1.
def multiply(a: int, b: int) -> int:
    return a * b
print(multiply(10, 20))

# 2.
from typing import List
def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)
print(sum_numbers([10,20,30]))

#3.
from typing import Optional
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None
print(find_user(0))

# 4.
def process_input(value: str | int) -> str:
    return f"Ты передал: {value}"
print(process_input(10))

# 5.
class User:
    def __init__(self, name:str, age: int):
        self.name = name
        self.age = age

    def green(self) -> str:
        return f"Привет, меня зовут {self.name}, мне {self.age}!"

user = User('Lex', 20)
print(user.green())


# 6.
def get_even_numbers(numbers: list[int]) -> list[int]:
    return [num for num in numbers if num % 2 == 0]
print(get_even_numbers([1, 2, 3]))