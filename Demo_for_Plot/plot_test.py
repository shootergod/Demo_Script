
import random
import plot_tools


# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    nums = []
    for _ in range(1000):
        nums.append(random.randint(1, 100))


    plot_tools.bar(data=nums)