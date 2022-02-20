input_prompt = "Please enter a valid url without quotation marks to append to your item notification list: "

link = input(input_prompt)
while len(link) > 0:
    with open('items.csv', 'a') as file:
        file.write('input_prompt\n')
    link = input(input_prompt)