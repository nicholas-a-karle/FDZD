import time
import random

print("Starting...")

# Values ///
tolerancex = 100
likablex = 0
angerx = 5
number = 0
DS = False

# Text ///////////////
print("-------")
user_input1 = input("Bill's Int Dialogue: ")
print(" ")
user_input2 = input("Player Answer 1: ")
print(" ")
user_input3 = input("Bill Response 1: ")
print(" ")
user_input4 = input("Player Answer 2: ")
print(" ")
user_input5 = input("Bill Response 2: ")
print(" ")
user_input6 = input("Player Answer 3: ")
print(" ")
user_input7 = input("Bill Response 3: ")
print(" ")
user_input8 = input("Player Answer 4: ")
print(" ")
user_input9 = input("Bill Response 4: ")
print(" ")
user_input10 = input("Bill No Response: ")
print("-------")

# For Solo Question
NPCText = "Bill: " + user_input1
Answer1 = "1. " + user_input2
NPCResponse1 = "Bill: " + user_input3
Answer2 = "2. " + user_input4
NPCResponse2 = "Bill: " + user_input5
Answer3 = "3. " + user_input6
NPCResponse3 = "Bill: " + user_input7
Answer4 = "4. " + user_input8
NPCResponse4 = "Bill: " + user_input9
NPCResponse5 = "Bill: " + user_input10



def Event():
    print(NPCText)
    time.sleep(1)
    print(" ")
    print(Answer1)
    print(Answer2)
    print(Answer3)
    print(Answer4)

    time.sleep(1)
    print(" ")
    number = int(input("Answer: "))
    print(" ")

    if number == 1:
        time.sleep(2)
        print(NPCResponse1)
    elif number == 2:
        time.sleep(2)
        print(NPCResponse2)
    elif number == 3:
        time.sleep(2)
        print(NPCResponse3)
    elif number == 4:
        time.sleep(2)
        print(NPCResponse4)
    time.sleep(1)

Event()

print("Code Complete")