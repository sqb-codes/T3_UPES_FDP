dataset = [
    "hello how are you ?",
    "I am good how about you ?",
    "I am all good",
    "Hello all good ?"
    ]

# 1. Map Phase
def mapper(data):
    mapper_output = []
    for line in data:
        words = line.split()
        for word in words:
            mapper_output.append((word.lower(), 1))
    return mapper_output

# 2. Shuffle and Sort Phase
def shuffle_and_sort(mapper_output):
    data_group = {}
    for key, value in mapper_output:
        if key in data_group:
            data_group[key].append(value)
        else:
            data_group[key] = [value]
    return data_group

# 3. Reduce Phase
def reducer(data_group):
    output = {}
    for key in data_group:
        output[key] = sum(data_group[key])
    return output

mapper_output = mapper(dataset)
data_group = shuffle_and_sort(mapper_output)
result = reducer(data_group)
print(result)