import torch
import torch.nn.functional as F
import math

x = torch.tensor([4., 6., 10., 14.])

sqrt2 = math.sqrt(2)

L = (x[0::2] + x[1::2]) / sqrt2
H = (x[0::2] - x[1::2]) / sqrt2

print("x =", x)
print("L =", L)
print("H =", H)