def hcfnaive(a, b):
    if b == 0:
        return a
    else:
        return hcfnaive(b, a % b)


output = 0
number = 987820
for i in range(number):
    if hcfnaive(number, i) == 1:
        output += i

print(output)
