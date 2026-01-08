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

 Processing Times:
Ground Truth:   3.7431 seconds
Misra-Gries:    3.0625 seconds
Lossy Counting: 3.7410 seconds

 Average Errors for Heavy Hitters (Threshold: 0.0010%)
Misra-Gries:    Avg Absolute Error: 1667.45, Avg Relative Error: 23.03%
Lossy Counting: Avg Absolute Error: 17.64, Avg Relative Error: 0.40%


# Count-Min Sketch
Processing completed in 10.63 seconds.
Count-Min Sketch Configuration:
  Width: 10,000
  Depth: 5
  Total cells: 50,000
  Approximate memory: 1758.20 KB (1.72 MB)
Top 10 Most Frequent Queries
 1. google                                             | Actual: 32163 | Estimated: 32407
 2. yahoo                                              | Actual: 13646 | Estimated: 13856
 3. ebay                                               | Actual: 13075 | Estimated: 13349
 4. yahoo.com                                          | Actual:  8743 | Estimated:  8927
 5. mapquest                                           | Actual:  8719 | Estimated:  8984
 6. myspace.com                                        | Actual:  8587 | Estimated:  8795
 7. google.com                                         | Actual:  7985 | Estimated:  8265
 8. myspace                                            | Actual:  6877 | Estimated:  7246
 9. www.yahoo.com                                      | Actual:  4240 | Estimated:  4469
10. internet                                           | Actual:  4207 | Estimated:  4426

Overall Error Metrics for Heavy Hitters (Threshold: 0.001)
Average Absolute Error for Heavy Hitters: 247.27
Average Relative Error for Heavy Hitters: 3.40%


