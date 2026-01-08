## Results based on first iteration.

# Lossy Counting & Misra-Gries Runtime
Parameters: Epsilon=0.0005, MG-k=2000
------------------------------------------------------------
Results:
Processing Time:      6.8989s
Ground Truth Size:    136860.86 KB (1216652 keys)
Lossy Counting Size:  473.63 KB (1624 keys)
Misra-Gries Size:     265.46 KB (1965 keys)
------------------------------------------------------------
Query                | Actual   | LC Est   | MG Est
google               | 32163    | 32163    | 30492   
yahoo                | 13646    | 13646    | 11975   
ebay                 | 13075    | 13075    | 11404
yahoo.com            | 8743     | 8740     | 7072
mapquest             | 8719     | 8716     | 7048   

# Count-Min Sketch
Count-Min Sketch Configuration:
  Width: 10,000
  Depth: 5
  Total cells: 50,000
  Approximate memory: 120 bytes
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