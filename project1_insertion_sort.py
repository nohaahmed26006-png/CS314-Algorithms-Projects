import time
import random
import copy

def insertion_sort(arr):
    a = copy.deepcopy(arr)
    n = len(a)
    comparisons = 0
    shifts = 0
    
    start_time = time.perf_counter()
    
    for j in range(1, n):
        key = a[j]
        i = j - 1
        
        while i >= 0:
            comparisons += 1
            if a[i] > key:
                a[i + 1] = a[i]
                shifts += 1
                i -= 1
            else:
                break
        a[i + 1] = key
        
    exec_time_ms = (time.perf_counter() - start_time) * 1000
    return a, comparisons, shifts, exec_time_ms

def run_experiments():
    sizes = [100, 500, 1000, 2000, 4000]
    print("=" * 80)
    print(f"{'n':<6} | {'Case Type':<15} | {'Comparisons':<14} | {'Shifts':<12} | {'Time (ms)':<10}")
    print("=" * 80)
    
    for n in sizes:
        sorted_arr = list(range(n))
        _, best_comp, best_shift, best_time = insertion_sort(sorted_arr)
        print(f"{n:<6} | {'Best (Sorted)':<15} | {best_comp:<14} | {best_shift:<12} | {best_time:<10.3f}")
        
        rev_arr = list(range(n, 0, -1))
        _, worst_comp, worst_shift, worst_time = insertion_sort(rev_arr)
        print(f"{n:<6} | {'Worst (Reverse)':<15} | {worst_comp:<14} | {worst_shift:<12} | {worst_time:<10.3f}")
        
        rand_arr = [random.randint(1, 100000) for _ in range(n)]
        _, avg_comp, avg_shift, avg_time = insertion_sort(rand_arr)
        print(f"{n:<6} | {'Average (Random)':<15} | {avg_comp:<14} | {avg_shift:<12} | {avg_time:<10.3f}")
        print("-" * 80)

if __name__ == "__main__":
    run_experiments()
