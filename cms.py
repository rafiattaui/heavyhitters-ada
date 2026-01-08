import sys
import hashlib
from collections import defaultdict
from typing import List, Tuple
import time
import hashlib

class CountMinSketch:
    def __init__(self, width: int = 10000, depth: int = 5):
        self.width = width
        self.depth = depth
        # Use 1D list or array.array for better cache locality and memory
        self.table = [[0] * width for _ in range(depth)]

    def add(self, item: str, count: int = 1):
        item = item.lower().strip()
        # Pre-calculate two basic hashes
        h1 = int(hashlib.md5(item.encode('utf-8')).hexdigest(), 16)
        h2 = int(hashlib.sha1(item.encode('utf-8')).hexdigest(), 16)
        
        for i in range(self.depth):
            # Kirsch-Mitzenmacher: hash_i = h1 + i * h2
            index = (h1 + i * h2) % self.width
            self.table[i][index] += count

    def estimate(self, item: str) -> int:
        item = item.lower().strip()
        h1 = int(hashlib.md5(item.encode('utf-8')).hexdigest(), 16)
        h2 = int(hashlib.sha1(item.encode('utf-8')).hexdigest(), 16)
        
        res = float('inf')
        for i in range(self.depth):
            index = (h1 + i * h2) % self.width
            res = min(res, self.table[i][index])
        return int(res)

    def get_stats(self) -> dict:
        return {
            'width': self.width,
            'depth': self.depth,
            'total_cells': self.width * self.depth,
            'memory_bytes': sys.getsizeof(self.table)
        }

def process_aol_dataset(filepath: str, cms: CountMinSketch) -> Tuple[int, dict]:
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


def main():
    filepath = "user-ct-test-collection-01.txt"
    width = 10000
    depth = 5
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    
    print("Count-Min Sketch for AOL Dataset")
    
    cms = CountMinSketch(width=width, depth=depth)

    startTime = time.perf_counter()
    
    total_queries, query_freq = process_aol_dataset(filepath, cms)

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
    print(f"  Total cells: {stats['total_cells']:,}")
    print(f"  Approximate memory: {stats['memory_bytes']:,} bytes")
    

    print("Top 10 Most Frequent Queries")
    top_queries = get_top_queries(query_freq, 10)
    for rank, (query, count) in enumerate(top_queries, 1):
        estimated = cms.estimate(query)
        print(f"{rank:2d}. {query[:50]:<50} | Actual: {count:5d} | Estimated: {estimated:5d}")
    
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