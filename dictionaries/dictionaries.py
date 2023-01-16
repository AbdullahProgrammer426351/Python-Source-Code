# dictionaries are like hashmap in java
dic = {
    "Harry": "Humman being",
    "Spoon": "Object"
}

# 1. method 1 to get value
print(dic["Harry"])

 # this will throw error if key does't exist
# 2. method 2 to get value
print(dic.get("Harry"))
# this is print None if key doesn't exists


# get all keys
print("Keys --> ", dic.keys())
# get all values
print(dic.values())
# get all items with key value pair
print(dic.items())

# traversal with for loop
for key in dic:
    print(key, " " , dic[key])

# traversal with for loop and f-string
for key in dic.keys():
    print(f"The value corresponding to the {key} is : {dic[key]}")



# get all keys and values in tuple
for key, value in dic.items():
    print(f"The value corresponding to the {key} is : {value}")