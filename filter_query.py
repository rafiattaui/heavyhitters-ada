import sys

def filter_aol_queries(input_file, clean_output, invalid_output):
    """
    Reads an AOL search log file, writes:
      - valid query lines to clean_output
      - invalid (empty/dash) query lines to invalid_output
    """

    def is_invalid_query(query):
        # Normalize
        q = query.strip()
        invalids = ['', '-', '""', "''"]
        # consider blank / whitespace as invalid
        return not q or q in invalids

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(clean_output, 'w', encoding='utf-8') as fout_clean, \
         open(invalid_output, 'w', encoding='utf-8') as fout_invalid:

        for line in fin:
            parts = line.split('\t')
            # If line too short or missing query field -> treat as invalid
            if len(parts) < 2:
                fout_invalid.write(line)
                continue

            query = parts[1]
            if is_invalid_query(query):
                fout_invalid.write(line)
            else:
                fout_clean.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python filter_aol.py <input log> <clean out> <invalid out>")
        sys.exit(1)

    input_log = sys.argv[1]
    clean_file = sys.argv[2]
    invalid_file = sys.argv[3]

    filter_aol_queries(input_log, clean_file, invalid_file)
    print(f"Done! Clean queries → {clean_file}, invalid → {invalid_file}")
