from __future__ import print_function

import sys
import numpy as np
from random import seed
import random
from time import time
import matplotlib.pyplot as plt 

sys.path.append('/home/xilinx')
from pynq import Overlay
from pynq import allocate

if __name__ == "__main__":
    print("Entry:", sys.argv[0])
    print("System argument(s):", len(sys.argv))

    print("Start of \"" + sys.argv[0] + "\"")

    ol = Overlay("/home/xilinx/IPbitFile/r09943020/diff/bd.bit")
    ipFP_ACCUM = ol.diff_sq_acc_0

    # generate random number
    seed(1)
    window0 = []
    window1 = []
    golden = 0
    for i in range(16):
        window0.append(random.randint(0,10))
        window1.append(random.randint(0,10))

    # allocate input array
    inBuffer0 = allocate(shape=(16), dtype=np.int16)
    inBuffer1 = allocate(shape=(16), dtype=np.int16)
    for i in range(16):
        inBuffer0[i] = np.int16(window0[i])
        inBuffer1[i] = np.int16(window1[i])
        golden += (window0[i]-window1[i])**2

    timeKernelStart = time()
    
    # setup the ip ...
    ipFP_ACCUM.write(0x10, inBuffer0.device_address)
    ipFP_ACCUM.write(0x18, inBuffer1.device_address)
    
    ipFP_ACCUM.write(0x00, 0x01)
    while (ipFP_ACCUM.read(0x00) & 0x4) == 0x0:
        continue
    timeKernelEnd = time()
    print("============================")
    print("Kernel execution time: " + str(timeKernelEnd - timeKernelStart) + " s")

    hw_res_first = ipFP_ACCUM.read(0x20)
    hw_res_second = ipFP_ACCUM.read(0x24)
    
    total_error = 0.0
    hw_res = hw_res_first + np.int64(hw_res_second*(2**32))
    total_error = golden - hw_res
    if(total_error<0):
        total_error = 0-total_error
    print("HW_res: ", hw_res)
    print("SW_res: ", golden)
    print("total_error: ", total_error)
    if (total_error < 1.0):
        print("TEST OK!\n")
    else:
        print("TEST FAILED!\n")
      
    print("============================")
    print("Exit process")