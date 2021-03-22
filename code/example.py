import crypten
import torch
import numpy as np
from crypten.mpc import MPCTensor
crypten.init()
torch.set_num_threads(1)

import warnings;
warnings.filterwarnings("ignore")

import crypten.mpc as mpc
import crypten.communicator as comm
@mpc.run_multiprocess(world_size=2)
def classify():
    client = crypten.load_from_party("client_hash.pth",src=0)[0]
    batch = crypten.load_from_party("batch_hash.pth",src=1)
    for x in batch:
        count = torch.count_nonzero((x-client).get_plain_text())
        if not count.is_nonzero():
            return True
    return False

@mpc.run_multiprocess(world_size=2)
def examine_conversion():
    x = torch.tensor([1, 2, 3])
    rank = comm.get().get_rank()
    x = MPCTensor(x, ptype=crypten.mpc.arithmetic)

    z=torch.tensor([1, 2, 3])
    z = MPCTensor(z, ptype=crypten.mpc.arithmetic)
    y = torch.tensor([0,0,0])
    check=x-z
    print(check.sign().get_plain_text())
    #print(part2.get_plain_text())


k = examine_conversion()
#print(classify())
