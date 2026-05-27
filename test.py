import time
while True:
    user_input = input('Enter password: ->')
    if user_input == '1234':
        print('Correct password!')
        time.sleep(1)
        print('Access granted')
        time.sleep(3)
        print('...')
        break