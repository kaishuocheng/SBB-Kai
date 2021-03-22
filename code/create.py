import crypten
import torch
import random
crypten.init()
torch.set_num_threads(1)
from crypten import mpc

NUM=10
BATCH_SIZE=5
@mpc.run_multiprocess(world_size=2)
def main():
    coin = random.randint(0,1)
    client_hash=torch.randn(1,NUM)
    batch_hash=[]
    for i in range(BATCH_SIZE-1):
        batch_hash.append(torch.randn(1,NUM)[0])
    if coin == 0:
        batch_hash.append(client_hash[0])
    else:
        batch_hash.append(torch.randn(1,NUM)[0])
    batch_hash=torch.stack(batch_hash)
    crypten.save_from_party(client_hash, "client_hash.pth",src=0)
    crypten.save_from_party(batch_hash, "batch_hash.pth",src=1)
main()
