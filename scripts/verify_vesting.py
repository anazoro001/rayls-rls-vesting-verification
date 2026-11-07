#!/usr/bin/env python3
"""Read-only RPC snapshot starter. No transaction signing or writes."""
import argparse, json, requests, datetime

LOCK="0x1463889D3a5EAAEE3f066d1CF438A8957F7Db98E"
TOKEN="0x07e17E17E17E17E17E17E17E17E17E17E17E17EA"
# Selectors transcribed from the explorer's displayed read methods.
CALLS={
 "actualBalance()":("0x39d1f908",LOCK),
 "expectedBalance()":("0x329d0fa5",LOCK),
 "firstUnlockTime()":("0x1db0ad5a",LOCK),
 "nextUnlockTime()":("0xf8737bc0",LOCK),
 "totalAmount()":("0x1a39d8ef",LOCK),
 "totalBurned()":("0xd89135cd",LOCK),
 "totalClaimed()":("0x5d4ad2a1",LOCK),
 "trancheCount()":("0x59eb8224",LOCK),
 "tranchesClaimed()":("0x22fe97ca",LOCK),
 "claimable()":("0xaf38d757",LOCK),
 "isFullyFunded()":("0xaebc34e4",LOCK),
 "decimals()":("0x313ce567",TOKEN),
 "symbol()":("0x95d89b41",TOKEN),
}
def rpc(s,url,method,params):
    req={"jsonrpc":"2.0","id":1,"method":method,"params":params}
    r=s.post(url,json=req,timeout=30); r.raise_for_status()
    data=r.json()
    print(json.dumps({"request":req,"response":data},indent=2))
    if "error" in data: raise RuntimeError(data["error"])
    return data["result"]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--rpc",default="https://mainnet-rpc.rayls.com")
    ap.add_argument("--block",default="latest")
    args=ap.parse_args(); s=requests.Session()
    chain=rpc(s,args.rpc,"eth_chainId",[])
    block=rpc(s,args.rpc,"eth_getBlockByNumber",[args.block,False])
    if not block: raise SystemExit("Block not found")
    tag=hex(int(block["number"],16))
    print("SNAPSHOT",json.dumps({
      "chain_id":int(chain,16),"block_number":int(block["number"],16),
      "block_hash":block["hash"],
      "timestamp_utc":datetime.datetime.fromtimestamp(int(block["timestamp"],16),datetime.timezone.utc).isoformat(),
      "block_tag":tag},indent=2))
    for name,(selector,target) in CALLS.items():
        value=rpc(s,args.rpc,"eth_call",[{"to":target,"data":selector},tag])
        if name=="symbol()":
            raw=bytes.fromhex(value[2:]); off=int.from_bytes(raw[:32],"big")
            n=int.from_bytes(raw[off:off+32],"big"); decoded=raw[off+32:off+32+n].decode()
            print("DECODE",name,decoded)
        elif name=="isFullyFunded()": print("DECODE",name,bool(int(value,16)))
        else: print("DECODE",name,int(value,16))
if __name__=="__main__": main()
