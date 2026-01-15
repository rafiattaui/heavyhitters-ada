import sys
import hashlib
from collections import defaultdict
from typing import List, Tuple
import time
import hashlib
import zlib

class CountMinSketch:
    def __init__(self, width: int = 10000, depth: int = 5):

        # CMS's advatage is that it uses fixed memory and provides probabilistic estimates.
        # Width and depth determine the accuracy and confidence of the estimates.
        # No matter how large the input stream is, the memory used remains constant.
        self.width = width
        self.depth = depth
        # There's a lot of overhead with list of lists in Python, but it's simpler to implement.
        self.table = [[0] * width for _ in range(depth)]
        # Use 1D list or array.array for better cache locality and memory
        # Stores integers as 4-byte unsigned integers similar to C's uint32_t
        # Reducing overhead compared to list of lists
        # self.table = [array.array('I', [0] * width) for _ in range(depth)] using the array library, optional
        
    def _get_hashes(self, item: str):
        data = item.encode('utf-8')

        # Originally used hashlib.md5 and hashlib.sha1, but they are slower, since they are cryptographic hashes.
        # Using zlib's crc32 and adler32 for faster non-cryptographic hashing.
        # These produce 32-bit hash values, suitable for our needs.
        h1 = zlib.crc32(data) & 0xffffffff # Bitwise AND to ensure unsigned integer
        h2 = zlib.adler32(data) & 0xffffffff # Bitwise AND to ensure unsigned integer
        return h1, h2

    def add(self, item: str, count: int = 1):
        item = item.lower().strip()
        h1, h2 = self._get_hashes(item)
        for i in range(self.depth):
            index = (h1 + i * h2) % self.width
            self.table[i][index] += count

    def estimate(self, item: str) -> int:
        item = item.lower().strip()
        h1, h2 = self._get_hashes(item)
        res = float('inf')
        for i in range(self.depth):
            index = (h1 + i * h2) % self.width
            res = min(res, self.table[i][index])
        return int(res)

    def get_stats(self) -> dict:
        """Calculates deep memory for List of Lists structure."""
        # Start with the outer list
        total_mem = sys.getsizeof(self.table)
        for row in self.table:
            # Add the inner list structure
            total_mem += sys.getsizeof(row)
            # Add the size of every integer object in the row
            total_mem += sum(sys.getsizeof(cell) for cell in row)
            
        return {
            "width": self.width,
            "depth": self.depth,
            "memory_kb": total_mem / 1024,
            "memory_mb": total_mem / (1024 * 1024)
        }

def process_aol_dataset(filepath: str, cms: CountMinSketch, limit=None) -> Tuple[int, dict]:
    query_freq = defaultdict(int)
    total_queries = 0
    
    print(f"File path : {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline().lower()
            if not ('anon' in first_line or 'query' in first_line):
                parts = first_line.split('\t')
                if len(parts) >= 2:
                    query = parts[1].strip()
                    if query and query not in ['-', '', '""', "''"]:
                        cms.add(query)
                        query_freq[query] += 1
                        total_queries += 1
            
            for line_num, line in enumerate(f, start=2):
                if limit and line_num > limit:
                    break

                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                
                query = parts[1].strip()
                if query and query not in ['-', '', '""', "''"]:
                    cms.add(query)
                    query_freq[query] += 1
                    total_queries += 1
                
                if total_queries % 10000 == 0:
                    print(f"Total number of queries : {total_queries:,}")
    
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)
    
    return total_queries, dict(query_freq)


def get_top_queries(query_freq: dict, n: int = 10) -> List[Tuple[str, int]]:
    return sorted(query_freq.items(), key=lambda x: x[1], reverse=True)[:n]

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
    filepath = "clean.txt"
    width = 10000
    depth = 5
    limit = sys.argv[1] if len(sys.argv) > 1 else None
    if limit:
        limit = int(limit)
    
    print("Count-Min Sketch for AOL Dataset")
    
    cms = CountMinSketch(width=width, depth=depth)

    startTime = time.perf_counter()
    
    total_queries, query_freq = process_aol_dataset(filepath, cms, limit=limit)

    endTime = time.perf_counter()
    print(f"\nProcessing completed in {endTime - startTime:.2f} seconds.\n")
    unique_queries = len(query_freq)
    
    print("Statistics")
    print(f"Total queries processed: {total_queries:,}")
    print(f"Unique queries: {unique_queries:,}")
    
    stats = cms.get_stats()
    print(f"\nCount-Min Sketch Configuration:")
    print(f"  Width: {stats['width']:,}")
    print(f"  Depth: {stats['depth']}")
    print(f"  Total cells: {stats['width'] * stats['depth']:,}")
    print(f"  Approximate memory: {stats['memory_kb']:.2f} KB ({stats['memory_mb']:.2f} MB)")
    

    print("Top 10 Most Frequent Queries")
    top_queries = get_top_queries(query_freq, 10)
    for rank, (query, count) in enumerate(top_queries, 1):
        estimated = cms.estimate(query)
        print(f"{rank:2d}. {query[:50]:<50} | Actual: {count:5d} | Estimated: {estimated:5d}")

    avg_abs, avg_rel, _ = calculate_metrics(query_freq, {q: cms.estimate(q) for q in query_freq}, total_queries)

    print("\nOverall Error Metrics for Heavy Hitters (Threshold: 0.001)")
    print(f"\nAverage Absolute Error for Heavy Hitters: {avg_abs:.2f}")
    print(f"\nAverage Relative Error for Heavy Hitters: {avg_rel*100:.2f}%")
    
    print("Interactive Query Mode")
    print("Enter search queries to estimate their frequency.")
    print("Type 'quit' to stop or 'exit' to quit the program.\n")
    
    while True:
        try:
            query = input("Query: ").strip()
            if query.lower() == 'quit':
                break
            elif query.lower() == 'exit':
                print("\nExiting program...")
                sys.exit(0)
            elif query == '':
                continue
            
            estimate = cms.estimate(query)
            actual = query_freq.get(query.lower(), 0)
            
            print(f"  Estimated frequency: {estimate}")
            print(f"  Actual frequency: {actual}")
            if actual > 0:
                error = abs(estimate - actual)
                print(f"  Error: {error} ({error/actual*100:.2f}%)")
            print()
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except EOFError:
            break
        
    
    print("\nDone!")


if __name__ == "__main__":
    main()