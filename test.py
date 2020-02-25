import inflect
p = inflect.engine()


string='I have 33 Networking books, 20 Database books, and 8 Programming books.'

tokenized_string = string.split(' ')
merged_string = []

for word in tokenized_string:
    print(word)

    if word.isnumeric():
        # print("Number")
        word = p.number_to_words(int(word))
        merged_string.append(word)

    else:
        # print("Not Number")
        merged_string.append(word)

cleaned_string = ' '.join(merged_string)
print(cleaned_string)