def binary_search(l, item):
    if l[len(l) // 2] == item:return  len(l) // 2
    if len(l) == 1: return False
    if item > l[len(l) // 2]: return binary_search(l[len(l) // 2:], item) + len(l) // 2
    if item < l[len(l) // 2]: return binary_search(l[:len(l) // 2], item)


print(binary_search([1,2,3,4,5,6,8,9,11,20,24,32],20))
