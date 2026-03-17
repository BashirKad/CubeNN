def helper(arr):
    for i in range(9):
        if (not arr[i].locked):
            print(arr[i].color)
        else:
            print("locked")