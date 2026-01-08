import sys
import time
import collections

def run_ground_truth(filename):
    counts = collections.Counter()
    total = 0
    start = time.perf_counter()
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        next(f)
        for line in f:
            parts = line.split('\t')
            if len(parts) > 1:
                query = parts[1].lower().strip()
                if query and query not in ['-', '', '""', "''"]:
                    counts[query] += 1
                    total += 1
    duration = time.perf_counter() - start
    # Return: (Total Processed, The actual Counter object, Duration)
    return total, counts, duration

def run_loss_counting_test(filename, epsilon=0.0005):
    from lossy import LossyCounting 
    lc = LossyCounting(epsilon)
    start = time.perf_counter()
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        next(f)
        for line in f:
            parts = line.split('\t')
            if len(parts) > 1:
                query = parts[1].lower().strip()
                if query and query not in ['-', '', '""', "''"]:
                    lc.add(query)
    duration = time.perf_counter() - start
    # Return: (The counts dictionary inside LC, Duration)
    return lc.counts, duration

def run_misra_gries_test(filename, k=2000):
    candidates = {}
    start = time.perf_counter()
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        next(f)
        for line in f:
            parts = line.split('\t')
            if len(parts) > 1:
                query = parts[1].lower().strip()
                if not query or query in ['-', '', '""', "''"]: continue
                
                if query in candidates:
                    candidates[query] += 1
                elif len(candidates) < k - 1:
                    candidates[query] = 1
                else:
                    for key in list(candidates.keys()):
                        candidates[key] -= 1
                        if candidates[key] == 0:
                            del candidates[key]
    duration = time.perf_counter() - start
    # Return: (The candidate dictionary, Duration)
    return candidates, duration

def get_deep_size(obj, seen=None):
    if seen is None: seen = set()
    obj_id = id(obj)
    if obj_id in seen: return 0
    seen.add(obj_id)
    
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(get_deep_size(k, seen) + get_deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, collections.Counter)):
        size += sum(get_deep_size(i, seen) for i in obj)
    return size

def main():
    filename = "user-ct-test-collection-01.txt"
    eps = 0.0005
    k_val = int(1/eps)

    print(f"--- Processing AOL Dataset (2006) ---")
    
    # 1. Ground Truth
    total_n, gt_data, gt_time = run_ground_truth(filename)
    
    # 2. Misra-Gries
    mg_data, mg_time = run_misra_gries_test(filename, k=k_val)
    
    # 3. Lossy Counting
    lc_data, lc_time = run_loss_counting_test(filename, epsilon=eps)

    # OUTPUT REPORT
    print("\n" + "="*85)
    print(f"{'RANK':<5} | {'QUERY':<20} | {'ACTUAL':<10} | {'MG EST':<10} | {'LC EST':<10}")
    print("-" * 85)

    top_10 = gt_data.most_common(10)
    for rank, (query, actual) in enumerate(top_10, 1):
        mg_est = mg_data.get(query, 0)
        lc_est = lc_data.get(query, 0)
        
        # In Misra-Gries, if an item is present, its count is an underestimate
        # In Lossy Counting, if it's present, its count is an underestimate
        print(f"{rank:<5} | {query[:20]:<20} | {actual:<10} | {mg_est:<10} | {lc_est:<10}")

    print("\n" + "="*85)
    print("ALGORITHM STATISTICS:")
    print(f"Ground Truth RAM:   {get_deep_size(gt_data)/1024/1024:,.2f} MB")
    print(f"Misra-Gries RAM:    {get_deep_size(mg_data)/1024/1024:,.2f} MB")
    print(f"Lossy Counting RAM: {get_deep_size(lc_data)/1024/1024:,.2f} MB")
    print(f"Space Reduction:    {100 * (1 - get_deep_size(lc_data)/get_deep_size(gt_data)):.2f}%")

if __name__ == "__main__":
    main()