def maxProductSubArray(arr):
    n = len(arr)

    pre, suff = 1, 1
    ans = float("-inf")
    for i in range(n):
        if pre == 0:
            pre = 1
        if suff == 0:
            suff = 1
        pre *= arr[i]
        suff *= arr[n - i - 1]
        ans = max(ans, max(pre, suff))
    return ans


arr = [9, 2, 5, 3, 7, 11, 8, 10, 19, 6]
print("The maximum product subarray is:", maxProductSubArray(arr))
