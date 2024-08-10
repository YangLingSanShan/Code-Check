def calculate(input_str):
    hash_map = {0: 1}

    MODULO = 1000000007
    result = 0
    current = 0
    for index, char in enumerate(input_str):
        if char == '1':
            current -= 1
        else:
            current += 1

        result += (len(input_str) - index) * hash_map.get(current, 0)
        result %= MODULO
        hash_map[current] = hash_map.get(current, 0) + index + 2

    return result


for iteration in range(int(input())):
    user_input = input().strip()
    print(calculate(user_input))
