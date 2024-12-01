input_string = "do you think that maybe like, 1 in 10 people could be actually robots?"

hex_string = ""
for c in input_string.lower():
    if c in "0123456789abcdef":
        hex_string += c
    else:
        hex_string += "0"

padding = 3 - len(hex_string) % 3
print(len(hex_string), padding)
hex_string = hex_string + "0" * padding
string_length = len(hex_string) // 3
print(len(hex_string), string_length)

print(input_string)
print(hex_string)
output = ""
for i in range(3):
    portion = hex_string[i * string_length :]
    print(i * string_length * " " + portion)
    output += portion[:2]
print(output)
