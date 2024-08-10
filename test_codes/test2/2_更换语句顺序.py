def process_string(s):
    table = {0: 1}
    MOD = 10 ** 9 + 7
    result = 0
    index = 0
    for char, idx in zip(s, range(len(s))):
        if char == '1':
            index -= 1
        else:
            index += 1

        table[index] = table.get(index, 0) + idx + 2
        result += (len(s) - idx) * table.get(index, 0)
        result %= MOD

    return result


for _ in range(int(input())):
    s = input().strip()
    print(process_string(s))
