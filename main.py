import sys
import time
import collections
from lossy import LossyCounting
from misragries import misra_gries

def get_deep_size(obj):
    """Calculates memory size of a container and all the strings inside it."""
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in obj.items())
    elif isinstance(obj, (list, set, collections.Counter)):
        size += sum(sys.getsizeof(i) for i in obj)
    return size

def run_comparative_test(filename, epsilon=0.0005):
    # k for Misra-Gries is set to 1/epsilon to make them comparable
    k = int(1 / epsilon)
    
    lc = LossyCounting(epsilon)
    mg_candidates = {}
    ground_truth = collections.Counter()
    
    print(f"Comparing Algorithms on: {filename}")
    print(f"Parameters: Epsilon={epsilon}, MG-k={k}")
    print("-" * 60)
    
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            next(f)  # Skip header
            
            start_time = time.perf_counter()
            for line in f:
                columns = line.split('\t')
                if len(columns) > 1:
                    query = columns[1].lower().strip()
                    if not query: continue
                    
                    # 1. Update Ground Truth
                    ground_truth[query] += 1
                    
                    # 2. Update Lossy Counting
                    lc.add(query)
                    
                    # 3. Update Misra-Gries (One-Pass)
                    if query in mg_candidates:
                        mg_candidates[query] += 1
                    elif len(mg_candidates) < k - 1:
                        mg_candidates[query] = 1
                    else:
                        for key in list(mg_candidates.keys()):
                            mg_candidates[key] -= 1
                            if mg_candidates[key] == 0:
                                del mg_candidates[key]
            
            end_time = time.perf_counter()

        # Memory Analysis
        mem_lc = get_deep_size(lc.counts) + get_deep_size(lc.bucket_id)
        mem_mg = get_deep_size(mg_candidates)
        mem_gt = get_deep_size(ground_truth)
        
        print(f"Results:")
        print(f"Processing Time:      {end_time - start_time:.4f}s")
        print(f"Ground Truth Size:    {mem_gt / 1024:.2f} KB ({len(ground_truth)} keys)")
        print(f"Lossy Counting Size:  {mem_lc / 1024:.2f} KB ({len(lc.counts)} keys)")
        print(f"Misra-Gries Size:     {mem_mg / 1024:.2f} KB ({len(mg_candidates)} keys)")
        print("-" * 60)
        
        # Accuracy Check (Top 5)
        print(f"{'Query':<20} | {'Actual':<8} | {'LC Est':<8} | {'MG Est':<8}")
        for item, actual in ground_truth.most_common(5):
            lc_est = lc.counts.get(item, 0)
            mg_est = mg_candidates.get(item, 0)
            print(f"{item:<20} | {actual:<8} | {lc_est:<8} | {mg_est:<8}")

    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'.")

if __name__ == "__main__":
    run_comparative_test("user-ct-test-collection-01.txt")
