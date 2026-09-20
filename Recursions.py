import math
import sys
from itertools import islice
import time

# העלאת מגבלת עומק הרקורסיה
sys.setrecursionlimit(2000)


# שאלה 1

# 1.א - רקורסיה רגילה
def make_tuple_reg(n=1000):
    if n <= 1:
        return (1,)
    return make_tuple_reg(n - 1) + (n,)

# 1.ב - רקורסיה זנבית
def make_tuple_tail(n=1000, current=1, acc=()):
    if current > n:
        return acc
    return make_tuple_tail(n, current + 1, acc + (current,))


# שאלה 2

# 2.א - רקורסיה רגילה
def sum_tuple_reg(t):
    if not t:
        return 0
    return t[0] + sum_tuple_reg(t[1:])

# 2.ב - רקורסיה זנבית
def sum_tuple_tail(t, acc=0):
    if not t:
        return acc
    return sum_tuple_tail(t[1:], acc + t[0])


# שאלה 3

# 3.א - רקורסיה רגילה (חישוב דרך GCD)
def gcd_reg(a, b):
    if b == 0:
        return a
    return gcd_reg(b, a % b)
def lcm_reg(a, b):
    return (a * b) // gcd_reg(a, b)

# 3.ב - רקורסיה זנבית
def lcm_tail(a, b, multiple=None):
    if multiple is None:
        multiple = max(a, b)
    if multiple % a == 0 and multiple % b == 0:
        return multiple
    return lcm_tail(a, b, multiple + max(a, b))


# שאלה 4

# 4.א - רקורסיה רגילה
def is_palindrome_number_reg(n):
    s = str(n)
    if len(s) <= 1:
        return True
    return (s[0] == s[-1]) and is_palindrome_number_reg(s[1:-1])

# 4.ב - רקורסיה זנבית
def is_palindrome_number_tail(n, left=0, right=None):
    s = str(n)
    if right is None:
        right = len(s) - 1
    if left >= right:
        return True
    if s[left] != s[right]:
        return False
    return is_palindrome_number_tail(n, left + 1, right - 1)


# שאלה 5

def clean_text(text):
    text = text.lower()
    hebrew_map = str.maketrans({'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'})
    text = text.translate(hebrew_map)
    return ''.join(filter(str.isalnum, text))

# 5.א - רקורסיה רגילה
def is_palindrome_alphanumeric_reg(text):
    cleaned = clean_text(text)
    def _check(s):
        if len(s) <= 1:
            return True
        return (s[0] == s[-1]) and _check(s[1:-1])
    return _check(cleaned)

# 5.ב - רקורסיה זנבית
def is_palindrome_alphanumeric_tail(text):
    cleaned = clean_text(text)
    def _check_tail(s, left=0, right=None):
        if right is None:
            right = len(s) - 1
        if left >= right:
            return True
        if s[left] != s[right]:
            return False
        return _check_tail(s, left + 1, right - 1)
    return _check_tail(cleaned)


# שאלה 6

# 6.א - רקורסיה רגילה
def sort_lists_reg(lists):
    if not lists:
        return []
    return [sorted(lists[0])] + sort_lists_reg(lists[1:])
def sortedzip_reg(lists):
    return zip(*sort_lists_reg(lists))

# 6.ב - רקורסיה זנבית
def sort_lists_tail(lists, acc=()):
    if not lists:
        return acc
    return sort_lists_tail(lists[1:], acc + (sorted(lists[0]),))
def sortedzip_tail(lists):
    return zip(*sort_lists_tail(lists))


# שאלה 7

# 7.א - רקורסיה רגילה
def encode_rle_reg(s):
    if not s:
        return ""
    def count_prefix(text, char):
        if not text or text[0] != char:
            return 0
        return 1 + count_prefix(text[1:], char)
    count = count_prefix(s, s[0])
    return f"{s[0]}{count}" + encode_rle_reg(s[count:])

# 7.ב - רקורסיה זנבית
def encode_rle_tail(s, acc=""):
    if not s:
        return acc
    def get_prefix_count(text, char, count=0):
        if not text or text[0] != char:
            return count, text
        return get_prefix_count(text[1:], char, count + 1)
    count, rest = get_prefix_count(s, s[0])
    return encode_rle_tail(rest, acc + f"{s[0]}{count}")


# Lazy Evaluation & Generators

# שאלה 1

def eager_evaluation():
    start_time = time.perf_counter()
    full_array = list(range(10001))
    exec_time = time.perf_counter() - start_time
    memory_size = sys.getsizeof(full_array)

    start_sub = time.perf_counter()
    sub_array = full_array[:5000]
    sub_time = time.perf_counter() - start_sub
    sub_memory = sys.getsizeof(sub_array)

    print("=== Eager Evaluation ===")
    print(f"Full Array -> Time: {exec_time:.8f}s, Memory: {memory_size} bytes, Type: {type(full_array)}")
    print(f"Sub Array  -> Time: {sub_time:.8f}s, Memory: {sub_memory} bytes, Type: {type(sub_array)}")
    print(f"Same Type? {type(full_array) == type(sub_array)}\n")


def lazy_evaluation():
    start_time = time.perf_counter()
    full_gen = (x for x in range(10001))
    exec_time = time.perf_counter() - start_time
    memory_size = sys.getsizeof(full_gen)

    start_sub = time.perf_counter()
    sub_gen = (x for x in islice(full_gen, 5000))
    sub_time = time.perf_counter() - start_sub
    sub_memory = sys.getsizeof(sub_gen)

    print("=== Lazy Evaluation ===")
    print(f"Full Gen -> Time: {exec_time:.8f}s, Memory: {memory_size} bytes, Type: {type(full_gen)}")
    print(f"Sub Gen  -> Time: {sub_time:.8f}s, Memory: {sub_memory} bytes, Type: {type(sub_gen)}")
    print(f"Same Type? {type(full_gen) == type(sub_gen)}\n")


# שאלה 2

def is_prime(n):
    if n < 2:
        return False
    return all(n % i != 0 for i in range(2, int(math.isqrt(n)) + 1))

def prime_generator():
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1


# שאלה 3

def taylor_e_generator(x):
    current_sum = 0.0
    n = 0
    while True:
        current_sum += (x**n) / math.factorial(n)
        yield current_sum
        n += 1




if __name__ == "__main__":
    print("--- שאלה 1: יצירת Tuple ---")
    t_reg = make_tuple_reg(1000)
    t_tail = make_tuple_tail(1000)
    print(f"אורך הטופל ברקורסיה רגילה: {len(t_reg)}")
    print(f"אורך הטופל ברקורסיה זנבית: {len(t_tail)}")

    print("\n--- שאלה 2: סכום איברי ה-Tuple ---")
    print(f"סכום (רקורסיה רגילה): {sum_tuple_reg(t_reg)}")
    print(f"סכום (רקורסיה זנבית): {sum_tuple_tail(t_tail)}")

    print("\n--- שאלה 3: LCM ---")
    print(f"LCM(6, 4) (רקורסיה רגילה): {lcm_reg(6, 4)}")
    print(f"LCM(6, 4) (רקורסיה זנבית): {lcm_tail(6, 4)}")

    print("\n--- שאלה 4: בדיקת פלינדרום למספר ---")
    print(f"האם 123454321 פלינדרום? (רגילה): {is_palindrome_number_reg(123454321)}")
    print(f"האם 123454321 פלינדרום? (זנבית): {is_palindrome_number_tail(123454321)}")

    print("\n--- שאלה 5: סקריפט ראשי לפלינדרום אלפאנומרי ---")
    p_input = input("enter text:\n")
    if not p_input.strip():
        print("invalid input")
    else:
        print(is_palindrome_alphanumeric_reg(p_input))

    print("\n--- שאלה 6: sortedzip ---")
    sample_lists = [[3, 1, 2], [5, 6, 4], ["a", "b", "c"]]
    print("sortedzip (Regular):", list(sortedzip_reg(sample_lists)))
    print("sortedzip (Tail):   ", list(sortedzip_tail(sample_lists)))

    print("\n--- שאלה 7: סקריפט ראשי לדחיסת RLE ---")
    rle_input = input("enter text:\n")
    if not rle_input.strip():
        print("invalid input")
    else:
        print(encode_rle_reg(rle_input))

    print("\n--- Lazy Evaluation שאלה 1: מדידות זיכרון וזמן ---")
    eager_evaluation()
    lazy_evaluation()

    print("--- Lazy Evaluation שאלה 2: 10 המספרים הראשוניים הראשונים ---")
    primes = prime_generator()
    for _ in range(10):
        print(next(primes), end=" ")
    print("\n")

    print("--- Lazy Evaluation שאלה 3: חישוב טור טיילור עבור e^2 ---")
    e_gen = taylor_e_generator(2)
    for _ in range(8):
        print(next(e_gen))