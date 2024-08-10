def get_result(s):
    t = {0: 1}

    MOD = 10**9 + 7
    res = 0
    cur = 0
    for ind, i in enumerate(s):
        cur = update_index(i, cur)
        res = update_result(ind, s, t, cur, res, MOD)
        t = update_table(ind, t, cur)

    return res

def update_index(i, cur):
    return cur - 1 if i == '1' else cur + 1

def update_result(ind, s, t, cur, res, MOD):
    res += (len(s) - ind) * t.get(cur, 0)
    res %= MOD
    return res

def update_table(ind, t, cur):
    t[cur] = t.get(cur, 0) + ind + 2
    return t

for _ in range(int(input())):
    s = input().strip()
    print(get_result(s))
