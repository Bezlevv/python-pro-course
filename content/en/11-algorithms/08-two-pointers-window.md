---
title: Two pointers and sliding window
summary: Techniques for subarray and pair problems.
order: 8
duration: 45 min
difficulty: advanced
tags: two pointers, sliding window
---

Two pointers and sliding windows turn O(n²) into O(n).

## Two-pointer sum

```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return left, right
        if s < target:
            left += 1
        else:
            right -= 1
    return None
```

## Sliding window

```python
def max_sum_window(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best
```

## Lesson summary

Move pointers by order; slide window to reuse sums.

<!--TASK-->
### Task 1 — Two sum
Implement two_sum_sorted.

### Task 2 — Test
Find pair for target 12 in [1,3,5,7].

### Task 3 — Max window
Compute max sum of size 3.

### Task 4 — Explain
Why O(n)?

### Task 5 — When sorted
When two pointers work?

### Task 6 — Window reuse
Explain how a sum is reused.

### Task 7 — Apply
Use window for longest substring idea.
<!--/TASK-->

<!--HINT-->
### Hint 1
While.

### Hint 2
(1, 4).

### Hint 3
Window.

### Hint 4
Each element once.

### Hint 5
Sorted.

### Hint 6
Add/remove.

### Hint 7
Map.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return left, right
        if s < target:
            left += 1
        else:
            right -= 1
    return None
```

### Solution 2
```python
print(two_sum_sorted([1, 3, 5, 7], 12))   # (1, 4)
```

### Solution 3
```python
def max_sum_window(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best

print(max_sum_window([1, 4, 2, 10, 23, 3], 3))   # 35
```

### Solution 4
```python
# Каждый элемент обрабатывается константное число раз:
# два указателя/окно проходят массив один раз
```

### Solution 5
```python
# Отсортированный массив позволяет предсказать,
# какой указатель двигать
```

### Solution 6
```python
# Окно сдвигается: добавляем правый, убираем левый элемент
# — сумма переиспользуется
```

### Solution 7
```python
# Для длиннейшей подстроки без повторов:
# окно + set/словарь последних позиций
```
<!--/SOLUTION-->

<!--QUIZ-->
What is the two-pointer trick?
- Move from ends
- Scan twice
- Sort twice
- None
* Correct answer: Move from ends
Sorted.

When does it work?
- Sorted arrays
- Unsorted
- Any
- None
* Correct answer: Sorted arrays
Order.

What is a sliding window?
- Subarray moved
- Full array
- Pointer pair
- None
* Correct answer: Subarray moved
Fixed k.

What is the benefit?
- O(n)
- O(n²)
- O(1)
- None
* Correct answer: O(n)
Reuse.

What does left += 1 do?
- Increases sum
- Decreases
- Stops
- None
* Correct answer: Increases sum
Target bigger.

What does right -= 1 do?
- Decreases sum
- Increases
- Stops
- None
* Correct answer: Decreases sum
Target smaller.

What is window?
- Current subarray sum
- Full sum
- Max
- None
* Correct answer: Current subarray sum
Rolling.

What is best?
- Max found
- Min
- First
- None
* Correct answer: Max found
Answer.

When sum too small?
- Move left
- Move right
- Stop
- None
* Correct answer: Move left
Increase.

When sum too large?
- Move right
- Move left
- Stop
- None
* Correct answer: Move right
Decrease.

What is O(1) extra space?
- Two variables
- A list
- A dict
- None
* Correct answer: Two variables
Memory.

Is sliding window linear?
- Yes
- No
- Quadratic
- None
* Correct answer: Yes
O(n).
<!--/QUIZ-->
