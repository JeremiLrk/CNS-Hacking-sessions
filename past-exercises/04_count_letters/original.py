# ORIGINAL CODE — Count the Letters
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

letter_count = 0
letter_dict = {}

with open('wordlist.txt', 'r') as file:
    # EXPLAINED: Repeat the next indented lines for each possible value.
    for line in file:
        for letter in line:
            # EXPLAINED: Run the indented block only when this condition is true.
            if letter == '\n':
                continue
            letter_count += 1
            letter_dict[letter] = letter_dict.get(letter, 0) + 1

for each in letter_dict:
    letter_dict[each] = (letter_dict[each] / letter_count) * 100



# get frequencies of ciphertext
x = input("Enter the ciphertext: ")

cyphertext_dict = {}
input_letter_count = 0

for letter in x:
    # optional: ignore symbols
    if not letter.isalpha():
        continue
    input_letter_count += 1
    cyphertext_dict[letter] = cyphertext_dict.get(letter, 0) + 1


for each in cyphertext_dict:
    cyphertext_dict[each] = (cyphertext_dict[each] / input_letter_count) * 100


#sort both dictionaireis based on frequency
sorted_dict1 = dict(sorted(letter_dict.items(), key=lambda item: item[1], reverse=True))
sorted_dict2 = dict(sorted(cyphertext_dict.items(), key=lambda item: item[1], reverse=True))


print("English frequencies:")
print(sorted_dict1)

print("Ciphertext frequencies:")
print(sorted_dict2)

mapping = {}

english_letters = list(sorted_dict1.keys())
cipher_letters = list(sorted_dict2.keys())

for i in range(min(len(cipher_letters), len(english_letters))):
    mapping[cipher_letters[i]] = english_letters[i]

print("Mapping:")
print(mapping)

result = []
for each in x:
    if each in mapping:
        result.append(mapping[each])
    else:
        result.append(each)
print("Decrypted text:")
print(''.join(result))













