def resolve_string(s):
    history = {0: 1}

    MOD = 10**9 + 7
    total = 0
    offset = 0
    for idx, char in enumerate(s):
        offset = modify_offset(char, offset)
        total = update_total(idx, s, history, offset, total, MOD)
        history = update_history(idx, history, offset)

    return total

def modify_offset(char, offset):
    return offset - 1 if char == '1' else offset + 1

def update_total(idx, s, history, offset, total, MOD):
    total += (len(s) - idx) * history.get(offset, 0)
    total %= MOD
    return total

def update_history(idx, history, offset):
    history[offset] = history.get(offset, 0) + idx + 2
    return history

for _ in range(int(input())):
    s = input().strip()
    print(resolve_string(s))
