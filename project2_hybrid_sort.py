import time
import random

def insertion_sort_slice(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge(arr, left, mid, right):
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
        
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
        
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1

def hybrid_merge_sort(arr, left, right, k_threshold):
    if right - left + 1 <= k_threshold:
        insertion_sort_slice(arr, left, right)
        return
        
    if left < right:
        mid = (left + right) // 2
        hybrid_merge_sort(arr, left, mid, k_threshold)
        hybrid_merge_sort(arr, mid + 1, right, k_threshold)
        merge(arr, left, mid, right)

def benchmark_cutoff():
    n = 50000
    base_data = [random.randint(1, 1000000) for _ in range(n)]
    thresholds = [1, 4, 8, 16, 32, 64, 128]
    
    print("=" * 60)
    print(f"Hybrid Sort Benchmark on Random Array of Size n = {n}")
    print("=" * 60)
    print(f"{'Cutoff Threshold (k)':<25} | {'Execution Time (ms)':<20}")
    print("-" * 60)
    
    best_k = None
    min_time = float('inf')
    
    for k in thresholds:
        data_copy = base_data.copy()
        start = time.perf_counter()
        hybrid_merge_sort(data_copy, 0, len(data_copy) - 1, k)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert data_copy == sorted(base_data), "Sort failed!"
        
        if elapsed < min_time:
            min_time = elapsed
            best_k = k
            
        label = f"k = {k}" + (" (Pure Merge Sort)" if k == 1 else "")
        print(f"{label:<25} | {elapsed:<20.2f}")
        
    print("=" * 60)
    print(f"Optimal Cutoff found: k = {best_k} with time {min_time:.2f} ms")
    print("=" * 60)

if __name__ == "__main__":
    benchmark_cutoff()
