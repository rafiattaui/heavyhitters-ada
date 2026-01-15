import sys
import math
import collections
import time

class LossyCounting:
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.n = 0 
        self.counts = {}  
        self.bucket_id = {} 
        self.current_bucket = 1
        self.width = math.ceil(1 / epsilon)

    def add(self, item):
        self.n += 1
        if item in self.counts:
            self.counts[item] += 1
        else:
            self.counts[item] = 1
            self.bucket_id[item] = self.current_bucket - 1

        if self.n % self.width == 0:
            self._prune()
            self.current_bucket += 1

    def _prune(self):
        to_delete = [item for item in self.counts 
        if self.counts[item] + self.bucket_id[item] <= self.current_bucket]
        for item in to_delete:
            del self.counts[item]
            del self.bucket_id[item]

def get_deep_size(obj):
    """Calculates memory size of a container and all the strings inside it."""
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in obj.items())
    elif isinstance(obj, (list, set, collections.Counter)):
        size += sum(sys.getsizeof(i) for i in obj)
    return size

def run_aol_local_test(filename):
    epsilon = 0.0005  
    lc = LossyCounting(epsilon)
    ground_truth = collections.Counter()
    
    print(f"Reading local file: {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            next(f) 
            
            start_time = time.perf_counter()
            for line in f:
                columns = line.split('\t')
                if len(columns) > 1:
                    query = columns[1].lower().strip()
                    if query:
                        lc.add(query)
                        ground_truth[query] += 1
            end_time = time.perf_counter()

        mem_lc = get_deep_size(lc.counts) + get_deep_size(lc.bucket_id)
        mem_gt = get_deep_size(ground_truth)
        
        print(f"ALGORITHM ANALYSIS: {filename}")
        print("-"*45)
        print(f"Total Queries Processed: {lc.n}")
        print(f"Processing Time:         {end_time - start_time:.4f} seconds")
        print(f"Lossy Counting Memory:   {mem_lc / 1024:.2f} KB")
        print(f"Ground Truth Memory:    {mem_gt / 1024:.2f} KB")
        print(f"Memory Saved:           {((mem_gt - mem_lc) / mem_gt) * 100:.2f}%")
        
        print("\nTOP HEAVY HITTERS (Accuracy Check):")
        print(f"{'Query Keyword':<20} | {'Actual':<8} | {'Estimated':<8} | {'Status'}")
        print("-" * 60)
        
        for item, actual_count in ground_truth.most_common(10):
            est_count = lc.counts.get(item, 0)
            status = "✅ OK" if est_count > 0 else "❌ PRUNED"
            print(f"{item:<20} | {actual_count:<8} | {est_count:<8} | {status}")

    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Please ensure it is in this folder.")

if __name__ == "__main__":
    run_aol_local_test("user-ct-test-collection-01.txt")