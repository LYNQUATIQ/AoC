def summable_components(target, n):

    if n == 1:
        return [str(target)]

    components_list = []
    for i in range(target + 1):
        components_list += [f"{i} {c}" for c in summable_components(target - i, n - 1)]
    return components_list


component_list = summable_components(123, 3)
total = 0
for components in component_list:
    print(components)
    total += components.count("1")
print(total)
