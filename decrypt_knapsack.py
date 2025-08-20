#!/usr/bin/env python3
import ast
import sys

def decrypt_knapsack(K, C):
    # 1) مرتب‌سازی K به صورت نزولی همراه با اندیس‌های اصلی
    indexed = sorted(enumerate(K), key=lambda x: x[1], reverse=True)
    B = [0] * len(K)
    rem = C

    # 2) greedy بر اساس بزرگ‌ترین مقدار
    for idx, value in indexed:
        if rem >= value:
            B[idx] = 1
            rem -= value

    # 3) تبدیل بیت‌ها به رشته باینری
    bitstr = ''.join(str(b) for b in B)
    print(f"[DEBUG] bitstr (len={len(bitstr)}):\n{bitstr}\n")

    # 4) باینری → عدد دسیمال M → رشته‌ی ده‌دهی
    M_int = int(bitstr, 2)
    M_str = str(M_int)
    print(f"[DEBUG] M (decimal concatenation):\n{M_str}\n")

    # 5) Backtracking برای تقسیم M_str به کدهای ASCII (32–126)
    from functools import lru_cache
    @lru_cache(None)
    def parse(idx):
        if idx == len(M_str):
            return []
        for length in (2, 3):
            if idx + length <= len(M_str):
                code = int(M_str[idx:idx+length])
                if 32 <= code <= 126:
                    rest = parse(idx+length)
                    if rest is not None:
                        return [code] + rest
        return None

    codes = parse(0)
    if codes is None:
        print("[ERROR] Failed to parse M_str into valid ASCII codes.", file=sys.stderr)
        sys.exit(1)

    return ''.join(chr(c) for c in codes)

if __name__ == "__main__":
    # بارگذاری K و C
    with open("knapsack_part1_add.txt", "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    namespace = {}
    import ast
    for line in lines:
        if line.startswith("K"):
            namespace['K'] = ast.literal_eval(line.split("=",1)[1].strip())
        elif line.startswith("C"):
            namespace['C'] = int(line.split("=",1)[1].strip())

    if 'K' not in namespace or 'C' not in namespace:
        print("[ERROR] Could not find K or C in file.", file=sys.stderr)
        sys.exit(1)

    K = namespace['K']
    C = namespace['C']

    plaintext = decrypt_knapsack(K, C)
    print("Decrypted plaintext:", plaintext)

