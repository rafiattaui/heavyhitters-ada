import sys
import time
import collections

def run_ground_truth(filename, max_lines=None):
    counts = collections.Counter()
    total = 0
    start = time.perf_counter()
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        next(f)
        for i,line in enumerate(f):
            if max_lines and i >= max_lines:
                break

            parts = line.split('\t')
            if len(parts) > 1:
                query = parts[1].lower().strip()
                if query and query not in ['-', '', '""', "''"]:
                    counts[query] += 1
                    total += 1
    duration = time.perf_counter() - start
    # Return: (Total Processed, The actual Counter object, Duration)
    return total, counts, duration

def run_loss_counting_test(filename, epsilon=0.0005, max_lines=None):
    from lossy import LossyCounting 
    lc = LossyCounting(epsilon)
    start = time.perf_counter()
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        next(f)
        for i,line in enumerate(f):
            if max_lines and i >= max_lines:
                break

            parts = line.split('\t')
            if len(parts) > 1:
                query = parts[1].lower().strip()
                if query and query not in ['-', '', '""', "''"]:
                    lc.add(query)
    duration = time.perf_counter() - start
    # Return: (The counts dictionary inside LC, Duration)
    return lc.counts, duration

def run_misra_gries_test(filename, k=2000, max_lines=None):
    candidates = {}
    start = time.perf_counter()
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        next(f)
        for i,line in enumerate(f):
            if max_lines and i >= max_lines:
                break

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
    """
    Recursively finds size of objects, including contents of containers.
    By default, it uses a set to track seen object ids to avoid double-counting.
    """
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

import csv
import os

def save_metrics_to_csv(
    csv_file,
    limit,
    mg_time, mg_mem, mg_ae, mg_re,
    lc_time, lc_mem, lc_ae, lc_re
):
    """
    Appends experiment metrics to a CSV file.
    Creates the file with header if it doesn't exist.
    """

    file_exists = os.path.isfile(csv_file)

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "limit",
                "mg_runtime", "mg_memory_kb", "mg_avg_abs_error", "mg_avg_rel_error",
                "lc_runtime", "lc_memory_kb", "lc_avg_abs_error", "lc_avg_rel_error"
            ])

        writer.writerow([
            limit,
            round(mg_time, 4), round(mg_mem, 2), round(mg_ae, 2), round(mg_re * 100, 2),
            round(lc_time, 4), round(lc_mem, 2), round(lc_ae, 2), round(lc_re * 100, 2)
        ])


def calculate_metrics(gt_data, algorithm_data, total_n, threshold_ratio=0.001):
    threshold = total_n * threshold_ratio
    abs_errors = []
    rel_errors = []
    
    # Only evaluate items that are actually "Heavy"
    heavy_hitters = {k: v for k, v in gt_data.items() if v >= threshold}
    
    for query, actual in heavy_hitters.items():
        est = algorithm_data.get(query, 0)
        error = abs(actual - est)
        abs_errors.append(error)
        rel_errors.append(error / actual)
        
    avg_abs = sum(abs_errors) / len(abs_errors) if abs_errors else 0
    avg_rel = sum(rel_errors) / len(rel_errors) if rel_errors else 0
    
    return avg_abs, avg_rel, len(heavy_hitters)

def main():
    filename = "clean.txt"
    eps = 0.0005
    limit = sys.argv[1] if len(sys.argv) > 1 else None
    if limit:
        limit = int(limit)
    k_val = int(1/eps)

    print(f"--- Processing AOL Dataset (2006) ---")
    
    # 1. Ground Truth
    total_n, gt_data, gt_time = run_ground_truth(filename, max_lines=limit)
    
    # 2. Misra-Gries
    mg_data, mg_time = run_misra_gries_test(filename, k=k_val, max_lines=limit)
    
    # 3. Lossy Counting
    lc_data, lc_time = run_loss_counting_test(filename, epsilon=eps, max_lines=limit)

    mg_mem = get_deep_size(mg_data) / 1024     # KB
    lc_mem = get_deep_size(lc_data) / 1024     # KB

    mg_avg_absolute_error, mg_avg_relative_error, mg_heavy_hitters_count = calculate_metrics(gt_data, mg_data, total_n)
    lc_avg_absolute_error, lc_avg_relative_error, lc_heavy_hitters_count = calculate_metrics(gt_data, lc_data, total_n)

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

    print("\n Processing Times:")
    print(f"Ground Truth:   {gt_time:.4f} seconds")
    print(f"Misra-Gries:    {mg_time:.4f} seconds")
    print(f"Lossy Counting: {lc_time:.4f} seconds")
    
    print("\n Average Errors for Heavy Hitters (Threshold: {:.4f}%)".format(0.001))
    print(f"Misra-Gries:    Avg Absolute Error: {mg_avg_absolute_error:.2f}, Avg Relative Error: {mg_avg_relative_error*100:.2f}%")
    print(f"Lossy Counting: Avg Absolute Error: {lc_avg_absolute_error:.2f}, Avg Relative Error: {lc_avg_relative_error*100:.2f}%")

    save_metrics_to_csv(
    csv_file="metrics.csv",
    limit=limit if limit else total_n,
    mg_time=mg_time,
    mg_mem=mg_mem,
    mg_ae=mg_avg_absolute_error,
    mg_re=mg_avg_relative_error,
    lc_time=lc_time,
    lc_mem=lc_mem,
    lc_ae=lc_avg_absolute_error,
    lc_re=lc_avg_relative_error
)

if __name__ == "__main__":
    main()