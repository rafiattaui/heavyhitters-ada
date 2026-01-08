## Results based on first iteration.

# Lossy Counting & Misra-Gries Runtime
--- Processing AOL Dataset (2006) ---

=====================================================================================
RANK  | QUERY                | ACTUAL     | MG EST     | LC EST
-------------------------------------------------------------------------------------
1     | google               | 32163      | 30492      | 32163     
2     | yahoo                | 13646      | 11975      | 13646     
3     | ebay                 | 13075      | 11404      | 13075
4     | yahoo.com            | 8743       | 7072       | 8740
5     | mapquest             | 8719       | 7048       | 8716
6     | myspace.com          | 8587       | 6916       | 8580
7     | google.com           | 7985       | 6314       | 7977
8     | myspace              | 6877       | 5209       | 6877
9     | www.yahoo.com        | 4240       | 2579       | 4173
10    | internet             | 4207       | 2547       | 4159

=====================================================================================
ALGORITHM STATISTICS:
Ground Truth RAM:   101.18 MB
Misra-Gries RAM:    0.21 MB
Lossy Counting RAM: 0.19 MB
Space Reduction:    99.81%


# Count-Min Sketch
Count-Min Sketch Configuration:
  Width: 10,000
  Depth: 5
  Total cells: 50,000
  Approximate memory: 1563.01 KB (1.53 MB)
Top 10 Most Frequent Queries
 1. google                                             | Actual: 32163 | Estimated: 32426
 2. yahoo                                              | Actual: 13646 | Estimated: 13846
 3. ebay                                               | Actual: 13075 | Estimated: 13354
 4. yahoo.com                                          | Actual:  8743 | Estimated:  8976
 5. mapquest                                           | Actual:  8719 | Estimated:  8965
 6. myspace.com                                        | Actual:  8587 | Estimated:  8806
 7. google.com                                         | Actual:  7985 | Estimated:  8243
 8. myspace                                            | Actual:  6877 | Estimated:  7126
 9. www.yahoo.com                                      | Actual:  4240 | Estimated:  4486
10. internet                                           | Actual:  4207 | Estimated:  4423