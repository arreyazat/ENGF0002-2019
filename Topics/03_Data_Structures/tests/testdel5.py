import time
lst = []
for length in range(1000, 1000000, 10000):
    while len(lst) < length:
        lst.append(42)
    count = 0
    starttime = time.time()
    while count < 200:
        #lst.pop(0)            # pop from start
        lst.pop()           # pop from end
        #lst.pop(length//2)  # pop from middle
        count += 1
    now = time.time()
    print(length, now - starttime)

