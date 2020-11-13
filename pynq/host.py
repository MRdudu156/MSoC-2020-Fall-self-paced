from __future__ import print_function

import sys

sys.path.append('/home/xilinx')
from pynq import Overlay

if __name__ == "__main__":
    print("Entry:", sys.argv[0])
    print("System argument(s):", len(sys.argv))

    print("Start of \"" + sys.argv[0] + "\"")

    ol = Overlay("/home/xilinx/IPBitFile/Multip2Num.bit")
    regIP = ol.top_atan2_0
    
    x0 = [-15,-15, -7, -7,-35,-35,-42,-42,-84,-84]
    y0 = [-14,-14, 34, 34,-42,-42,-32,-32, 74, 74]
    z_res = [-2.3217253685,-2.3217253685,-0.2030452192,-0.2030452192,-2.4468543530,-2.4468543530,-2.2218730450,-2.2218730450,-0.8486049771,-0.8486049771]
    for i in range(9):
        print("============================")
        regIP.write(0x10, y0[i])
        regIP.write(0x18, x0[i])
        while(regIP.read(0x24) & 0x1) == 0x0:
            continue
        Res = regIP.read(0x20)
        print("Rad of (x, y) = " + str(x0[i]) + str(y0[i]) + " : " + str(Res))
        print("Referencr ans is " + z_res[i])
    print("============================")
    print("Exit process")