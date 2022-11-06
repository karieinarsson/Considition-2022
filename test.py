from NN.chromosoneNN import Chromosone
import torch as th
import torch.nn as nn
import numpy as np
from random import randint

def main():
    for _ in range(100):
        c = Chromosone()
        print(c.get_order(1, 2))
   
if __name__ == "__main__":
    main()