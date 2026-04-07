def helper(arr):
    
    for i in range(4):
        if (not arr[i]["locked"]):
            print(i, ": ", arr[i]["color"])
        else:
            print("locked")
    print("\n")             