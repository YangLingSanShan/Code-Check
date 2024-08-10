def solve(s):
    t = {0: 1}

    MOD = 10 ** 9 + 7
    res = 0
    cur = 0
    for ind, i in enumerate(s):
        if i == '1':
            cur -= 1
        else:
            cur += 1

        res += (len(s) - ind) * t.get(cur, 0)
        res %= MOD
        t[cur] = t.get(cur, 0) + ind + 2

    return res


for _ in range(int(input())):
    s = input().strip()
    print(solve(s))