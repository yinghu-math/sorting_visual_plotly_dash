def bubble_sort_steps(array_original):
    # best O(n), worst O(n^2)
    array = array_original[:]
    n = len(array)
    steps = [array[:], ]
    flag = 1
    while flag == 1:
        flag = 0
        for i in range(n-1):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
                flag = 1
                steps.append(array[:])
    return steps


def merge_sort_steps(array_original, steps = None):
    # O(nlogn)
    array = array_original[:]
    if steps is None:
        steps = [array[:], ]
    def merge_sort_helper(array, i, j, steps):
        if j - i < 2:
            return array[i : j]
        c = (i + j) // 2
        L = merge_sort_helper(array, i, c, steps)
        R = merge_sort_helper(array, c, j, steps)
        l = 0
        r = 0
        while l < (c - i) or r < (j - c):
            if l < (c - i) and r < (j - c):
                if L[l] <= R[r]:
                    array[i + l + r] = L[l]
                    l += 1
                else:
                    array[i + l + r] = R[r]
                    r += 1
            elif l == c-i:
                array[i + l + r] = R[r]
                r += 1
            else:
                array[i + l + r] = L[l]
                l += 1
            # remove the duplicate frames
            # program is not optimized
            if array[:] not in steps:
                steps.append(array[:])
        return array[i : j]
    merge_sort_helper(array, 0, len(array), steps)
    return steps

def quick_sort(array_original):
    # average O(nlog(n)), worst O(n^2), in place
    def partition(array, i, j):
        # The program returns the correct idx for the pivot; This is where we
        #   will partition the array.
        pivot = array[j-1]
        partition_idx = i - 1
        for idx in range(i, j-1):
            if array[idx] <= pivot:
                partition_idx += 1
                array[idx], array[partition_idx] = array[partition_idx], array[idx]
        array[partition_idx+1], array[j-1] = array[j-1], array[partition_idx+1]
        return partition_idx + 1

    def quick_sort_helper(array, low_idx, high_idx):
        if low_idx < high_idx:
            partition_idx = partition(array, low_idx, high_idx)
            quick_sort_helper(array, low_idx, partition_idx)
            quick_sort_helper(array, partition_idx+1, high_idx)
        return array

    array = array_original[:]
    return quick_sort_helper(array, 0, len(array))

print(quick_sort([4,2,1,5,0]))
