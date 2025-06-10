def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    count = 0
    upper_bound = None
 
    while low <= high:
 
        mid = (high + low) // 2
        count += 1
 
        if arr[mid] < x:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1
 
    # якщо елемент не знайдений
    return count, upper_bound


# Перевіряємо відпрацювання
arr = [1.2, 4.7, 5.8, 7.8, 9.8, 11.1, 13.3, 17.9, 19.3, 21.8]
x = 10

count, upper_bound = binary_search(arr, x)

print(f'Кількість ітерацій = {count}')
print(f'Верхня межа = {upper_bound}')