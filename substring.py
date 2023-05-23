class substring:
    # Алгоритм Бойера-Мора
    NO_OF_CHARS = 256

    def badCharHeuristic(string, size):
        badChar = [-1] * Substring.NO_OF_CHARS
        for i in range(size):
            badChar[ord(string[i])] = i
        return badChar

    def searchBM(txt, pat):
        m = len(pat)
        n = len(txt)
        badChar = Substring.badCharHeuristic(pat, m)
        s = 0
        while (s <= n - m):
            j = m - 1
            while j >= 0 and pat[j] == txt[s + j]:
                j -= 1
            if j < 0:
                print("Паттерн возникает при сдвиге = {}".format(s))
                s += (m - badChar[ord(txt[s + m])] if s + m < n else 1)
            else:
                s += max(1, j - badChar[ord(txt[s + j])])

    # Алгоритм Робин-Карпа
    def searchRK(pat, txt, q):
        M = len(pat)
        N = len(txt)
        i = 0
        j = 0
        p = 0
        t = 0
        h = 1
        for i in range(M - 1):
            h = (h * Substring.NO_OF_CHARS) % q
        for i in range(M):
            p = (Substring.NO_OF_CHARS * p + ord(pat[i])) % q
            t = (Substring.NO_OF_CHARS * t + ord(txt[i])) % q
        for i in range(N - M + 1):
            if p == t:
                for j in range(M):
                    if txt[i + j] != pat[j]:
                        break

                j += 1
                if j == M:
                    print("Шаблон, найденный по индексу " + str(i))
            if i < N - M:
                t = (Substring.NO_OF_CHARS * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q
                if t < 0:
                    t = t + q

    # Алгоритм Кнута-Морриса-Пратт
    def KMPSearch(pat, txt):
        M = len(pat)
        N = len(txt)
        lps = [0] * M
        j = 0
        Substring.computeLPSArray(pat, M, lps)

        i = 0
        while (N - i) >= (M - j):
            if pat[j] == txt[i]:
                i += 1
                j += 1

            if j == M:
                print("Обнаруженный паттерн по индексу " + str(i - j))
                j = lps[j - 1]

            elif i < N and pat[j] != txt[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

    def computeLPSArray(pat, M, lps):
        len = 0

        lps[0] = 0
        i = 1

        while i < M:
            if pat[i] == pat[len]:
                len += 1
                lps[i] = len
                i += 1
            else:
                if len != 0:
                    len = lps[len - 1]
                else:
                    lps[i] = 0
                    i += 1

    # Алгоритм на конечных автоматах
    def getNextState(pat, M, state, x):

        if state < M and x == ord(pat[state]):
            return state + 1

        i = 0

        for ns in range(state, 0, -1):
            if ord(pat[ns - 1]) == x:
                while (i < ns - 1):
                    if pat[i] != pat[state - ns + 1 + i]:
                        break
                    i += 1
                if i == ns - 1:
                    return ns
        return 0

    def computeTF(pat, M):

        TF = [[0 for i in range(Substring.NO_OF_CHARS)] \
              for _ in range(M + 1)]

        for state in range(M + 1):
            for x in range(Substring.NO_OF_CHARS):
                z = Substring.getNextState(pat, M, state, x)
                TF[state][x] = z

        return TF

    def searchEA(pat, txt):

        M = len(pat)
        N = len(txt)
        TF = Substring.computeTF(pat, M)

        state = 0
        for i in range(N):
            state = TF[state][ord(txt[i])]
            if state == M:
                print("Шаблон, найденный по индексу: {}". \
                      format(i - M + 1))