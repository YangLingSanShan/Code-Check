def evaluate_sequence(seq):
    lookup = {0: 1}
    mod_value = 10 ** 9 + 7
    answer = 0
    running_total = 0
    for position, digit in enumerate(seq):
        if digit == '1':
            running_total -= 1
        else:
            running_total += 1

        answer = (answer + (len(seq) - position) * lookup.get(running_total, 0)) % mod_value
        lookup[running_total] = lookup.get(running_total, 0) + position + 2

    return answer


for trial in range(int(input())):
    sequence = input().strip()
    print(evaluate_sequence(sequence))
