import multiprocessing
import numpy as np
import parmap

def square(input_list):
    return [x*x for x in input_list]


num_cores = multiprocessing.cpu_count()
data = list(range(1, 17))
split_data = np.array_split(data, num_cores)
print(split_data)
print()
test = [x.tolist() for x in split_data]

result = parmap.map(square, split_data, pm_pbar=True, pm_processes=num_cores)
print(result)