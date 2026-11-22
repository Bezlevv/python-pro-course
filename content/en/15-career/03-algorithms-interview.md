---
title: Algorithmic Problems in Interviews
summary: How to solve interview problems: complexity analysis, key patterns, and the "brute force to optimization" strategy.
order: 3
duration: 50 min
difficulty: advanced
tags: algorithms, complexity, two pointers, sliding window, binary search
---

Algorithmic problems are a mandatory part of developer interviews. They test not formula knowledge but the ability to think in a structured way: breaking a problem into parts, estimating efficiency, and pushing a solution to edge cases.

## Complexity analysis: Big O

Big O describes how execution time (or memory) grows as the input `n` grows:

- O(1) — constant: indexing into a list;
- O(log n) — logarithmic: binary search in a sorted array;
- O(n) — linear: one pass over an array;
- O(n log n) — fast sorts, `sorted()`;
- O(n²) — two nested loops;
- O(2^n) — exponential: enumerating all subsets.

Rule: ignore constants and lower-order terms: `3n + 100` is O(n), and `n² + n` is O(n²). When choosing a solution, always state the complexity out loud — the interviewer expects it.

## Key patterns

Most problems are solved with one of a limited set of techniques:

- **Hash table (dict)** — for O(1) lookups: "find a pair with a given sum", "count occurrences".
- **Two pointers** — for sorted arrays and strings: palindromes, finding pairs, merging.
- **Sliding window** — for subarrays of fixed or variable length: maximum sum, longest segment without repeats.
- **Binary search** — for sorted data: finding an element, finding a boundary.
- **Recursion + memoization** — for problems that split into subproblems: staircases, paths, Fibonacci numbers.
- **BFS/DFS** — for graphs and grids.

## Solution strategy

1. **Clarify** the input and output: what comes in, what to return, what to do with empty input.
2. **Give an example** on small data and walk through it by hand.
3. **Start with brute force** — a simple working solution. Then ask: where is the bottleneck? What could be stored in a dict?
4. **Optimize** one idea at a time, naming the new complexity.
5. **Check edge cases**: empty list, one element, duplicates, negative numbers, very large values.
6. **Wrap up**: make sure the code runs without errors.

## How to practice

Solve 1–2 problems a day on LeetCode or similar platforms. Study others' solutions and rewrite them by hand, not copy them. At the actual interview, talk out loud: the interviewer wants to see your thought process, not just the final code.

## Summary

Know the complexity of basic operations, keep five or six patterns in your head, and always start with a simple working solution. Practice turns algorithms from a scary topic into predictable problems.

<!--TASK-->
### Task 1
Here is the Two Sum problem: a function `two_sum(nums, target)` takes a list of integers `nums` and an integer `target` and returns the indices of the two elements whose sum equals `target`. It is guaranteed that a solution exists and is unique. Write an O(n) solution using a dictionary. Test it: `nums = [2, 7, 11, 15]`, `target = 9` — the function should return `[0, 1]`. Explain why the solution with two nested loops is slower.

### Task 2
Write a function `max_sum_k(nums, k)` that returns the maximum sum of a subarray of length `k`. For example, for `nums = [1, 4, 2, 10, 23, 3, 1, 0, 20]` and `k = 4` the answer is 39 (the sum of the subarray [4, 2, 10, 23]). Use the sliding window method: first compute the sum of the first `k` elements, then slide the window, adding the next element and removing the first one. Complexity — O(n). Verify the result on the example.

### Task 3
Write a function `binary_search(arr, target)` that finds the index of `target` in an ascending-sorted list `arr` and returns it, or returns -1 if the element is absent. Implement binary search yourself, without using standard library search methods. Test it: `arr = [1, 3, 5, 7, 9, 11]`, `target = 7` → `3`; `target = 4` → `-1`. Explain why the complexity is O(log n).

### Task 4
Write a function `is_palindrome(s)` that checks whether the string `s` is a palindrome, ignoring spaces, punctuation, and letter case. Use two pointers: one moving from the start, the other from the end. For example, `is_palindrome("A man, a plan, a canal, Panama")` should return `True`, and `is_palindrome("Python")` should return `False`. Pay attention to handling non-letter characters.

### Task 5
Write a function `climb_stairs(n)` that counts how many ways you can climb a staircase of `n` steps if each step can cover 1 or 2 stairs. For example, for `n = 3` the answer is 3 (1+1+1, 1+2, 2+1). Use dynamic programming without an array: store only the two last values. Check for `n = 4` (answer 5) and explain what sequence you get.

<!--/TASK-->

<!--HINT-->
### Hint 1
While walking through the list, store already-seen numbers and their indices in a dictionary. For each number `x`, check whether the value `target - x` is in the dictionary. This way you find the pair in one pass: complexity O(n), not O(n²). Don't forget to check that the number's index doesn't equal the current one.

### Hint 2
First compute the sum of the first window: `current = sum(nums[:k])`. Then in a loop from `k` to the end: `current += nums[i] - nums[i - k]` and update the maximum. This recomputes the sum in O(1) per step, and the whole algorithm is O(n). Compare with the naive version that computes each window's sum from scratch.

### Hint 3
Set up pointers `left = 0` and `right = len(arr) - 1`. While `left <= right`, take the middle `mid = (left + right) // 2`. If `arr[mid] == target` — return `mid`; if it's smaller — move `left = mid + 1`; if larger — `right = mid - 1`. After the loop return -1.

### Hint 4
Set up `left = 0` and `right = len(s) - 1`. While `left < right`: if the left character isn't a letter, advance `left`; if the right one isn't a letter, advance `right`; otherwise compare the characters in lowercase via `s[left].lower() == s[right].lower()`. If they differ, return `False`; otherwise advance both pointers. Check an empty string: it is a palindrome.

### Hint 5
The number of ways for `n` steps is the sum of ways for `n-1` and `n-2`: you can reach a step from the previous one or from two steps back. These are Fibonacci numbers shifted by one. Keep two variables `prev2 = 1` (for n=1) and `prev1 = 2` (for n=2), updating them in a loop. This way we avoid an array of size n.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

What's going on here? We walk through the list once. For each number `x` we look for its "complement" `target - x` in the dictionary. If it has appeared before — we found the pair: the complement's index from the dict and the current index. If not, we store the current number with its index. Complexity O(n) in time and O(n) in memory. The naive version with two nested loops is O(n²): for each element we would rescan the whole list. The dictionary turns complement lookup from O(n) into O(1).

### Solution 2
Solution:

```python
def max_sum_k(nums, k):
    if k > len(nums):
        return None
    current = sum(nums[:k])
    best = current
    for i in range(k, len(nums)):
        current += nums[i] - nums[i - k]
        best = max(best, current)
    return best

print(max_sum_k([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))  # 39
```

What's going on here? First we compute the sum of the first window of `k` elements. Then we slide the window one step: `nums[i]` is the new element on the right, `nums[i - k]` is the leaving element on the left. Recomputing the sum takes O(1), so the whole algorithm is O(n). The naive approach would recompute each window from scratch in O(k), giving O(n·k). The sliding window is one of the most common patterns — it fits fixed-length subarrays perfectly.

### Solution 3
Solution:

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9, 11], 7))  # 3
print(binary_search([1, 3, 5, 7, 9, 11], 4))  # -1
```

What's going on here? Binary search discards half of the array at each step: if the middle element is smaller than the target, the target is to the right, and we move `left`; if larger — to the left, we move `right`. After each comparison the search interval halves, so the number of steps is log2(n), and the complexity is O(log n). For 1,000,000 elements that's about 20 comparisons instead of a million in linear search. The `left <= right` condition guarantees we don't miss the element when the interval narrows to a single position.

### Solution 4
Solution:

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalpha():
            left += 1
            continue
        if not s[right].isalpha():
            right -= 1
            continue
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("A man, a plan, a canal, Panama"))  # True
print(is_palindrome("Python"))                        # False
```

What's going on here? Two pointers move toward each other. If a character is not a letter (space, punctuation), we skip it and advance the corresponding pointer. When we reach two letters, we compare them in lowercase: `lower()` removes the difference between 'A' and 'a'. If the letters don't match, we return `False`. If the pointers meet with no mismatches, it's a palindrome. Edge cases: an empty string and a single-character string return `True` — that's the standard expectation, and it's worth mentioning at the interview.

### Solution 5
Solution:

```python
def climb_stairs(n):
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1

print(climb_stairs(3))  # 3
print(climb_stairs(4))  # 5
```

What's going on here? You can reach step `n` only from `n-1` (a step of 1) or `n-2` (a step of 2). So the number of ways is `f(n) = f(n-1) + f(n-2)` — a Fibonacci sequence shifted by one position: f(1)=1, f(2)=2, f(3)=3, f(4)=5. Instead of an array of size n we store just two variables: `prev2` — ways for `n-2`, `prev1` — for `n-1`. At each step we update the pair. Complexity O(n) in time and O(1) in memory. If you didn't spot the formula, you could start with recursion, but that would be O(2^n) — memoization or an iterative recomputation solves that.

<!--/SOLUTION-->

<!--QUIZ-->
What is the complexity of two nested loops over an array of size n?
- O(n)
- O(n²)
- O(log n)
- O(1)
* Correct answer: O(n²)
Two nested loops perform n × n operations — O(n²).

Which data structure finds an element by key in O(1) on average?
- List
- Dictionary
- Tuple
- Queue
* Correct answer: Dictionary
A dict is backed by a hash table, so key lookup is almost instant.

What data is binary search suitable for?
- A sorted array
- Any list
- Strings of any length
- All data types
* Correct answer: A sorted array
Binary search requires sorted data; otherwise dividing in half is meaningless.

Which pattern fits finding the maximum sum of a fixed-length subarray?
- Sliding window
- Two pointers moving toward each other
- Binary search
- Recursion without memoization
* Correct answer: Sliding window
The window moves across the array and recomputes the sum in O(1) per step.

What should you check first when solving a problem?
- Edge cases: empty input, one element, duplicates
- Code beauty
- Variable names
- Comment length
* Correct answer: Edge cases: empty input, one element, duplicates
Edge cases break most naive solutions, so they are checked first.

What is the complexity of recursive Fibonacci without memoization?
- O(2^n)
- O(n)
- O(log n)
- O(1)
* Correct answer: O(2^n)
Each number computes two previous ones, so the call tree grows exponentially.

What is memoization?
- Caching function call results to avoid computing the same thing twice
- Loop optimization
- Splitting an array into parts
- Data sorting
* Correct answer: Caching function call results to avoid computing the same thing twice
Memoization turns exponential recursion into linear or polynomial.

Which sort runs in O(n log n) on average?
- Quicksort and merge sort
- Bubble sort
- Insertion sort
- Selection sort
* Correct answer: Quicksort and merge sort
These algorithms divide and conquer; bubble and insertion sort run in O(n²).

<!--/QUIZ-->
