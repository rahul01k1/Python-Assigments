# problem 1
def find_max(numbers):
    if not numbers:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num
nums = [3, 7, 2, 8, 4]
print("Maximum number is:", find_max(nums))


# problem 2
def addNumbers(a, b):
    result = a + b
    return result
number1 = int(input("Enter the first number:"))
number2 = int(input("Enter the second number:"))
sum = addNumbers(number1,number2)
print("The sum is:", sum)


# problem 3
def check_even_odd(num):
    if num % 2 == 0:
        print("The number is even.")
    else:
        print("The number is odd.")
number = int(input("Enter a number: "))
check_even_odd(number)

#problem 4
my_list = [10, 20]
print(my_list[0])
print(my_list[1])

try:
     print(my_list[2])
except IndexError as e:
     print("Error: ",e)

# problem 5
name = input("Enter your name: ")
age = int(input("Enter your age: "))
greeting = "Hello, " + name + ". You are " + str(age) + " years old."
print(greeting)
   

# problem 6
counter = 1
while counter <= 10:
    print(counter)
    counter += 1

# problem 7
for i in range(1, 6):
    print(i)

# problem 8
def multiply(a, b):
    result = a * b
    return result
result = multiply(5, 10)
print(result)

# problem 9
def calculate_area(length, width):
    return length * width
l = 10
w = 5
area = calculate_area(l,w) # Missing second argument
print("The area is:", area)

# problem 10
counter = 0
def increment_counter():
    global counter
    counter += 1
increment_counter()
print("Counter:", counter)

# problem 11
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
try:
    result = num1 / num2
    print("Result:", result)
except ZeroDivisionError as e:
    print("error",e)

# problem 12
try:
    file = open("data.txt", "r")
    content = file.read()
    print(content)
    file.close()
except FileNotFoundError as e:
    print("error:", e)