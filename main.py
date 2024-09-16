import random as r
random_num = r.randint(0,10)
attempts = 0
first_random = True
print(random_num)
while first_random == True:
    find = input("Guess number between 0 and 10: ")
    if find.isdigit() and int(find) or int(find) == 0:
        if int(find) == random_num:
            attempts +=1
            print(f"You found num with {attempts} attempts")
            first_random = False
        elif int(find) < random_num:
            print("Random num greater")
            attempts +=1
        elif int(find) > random_num:
            print("Random num smaller")
            attempts +=1
    else:
        print('Pls write number not str')
        attempts +=1
comp_attempts = 0
while first_random == False:
    print('pls think 1 number')
    user_check = input('Your number greater(+) or smaller(-) or equal(=)')
    if user_check == '=':
        comp_attempts += 1
        if attempts == comp_attempts:
            print(f"Draw your attempts {attempts} my attempts {comp_attempts}")
        elif attempts > comp_attempts:
            print(f"I'm won your attempts {attempts} my attempts {comp_attempts}")
        elif attempts < comp_attempts:
             print(f"You are won your attempts {attempts} my attempts {comp_attempts}")
        break
    elif user_check == '+':
        
