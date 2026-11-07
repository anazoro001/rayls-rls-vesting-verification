# Rayls RLS Vesting Verification

Research package for the Parfin `RlsTokenLock` contract on Rayls Public Chain.

- Lock: `0x1463889D3a5EAAEE3f066d1CF438A8957F7Db98E`
- Token: `0x07e17E17E17E17E17E17E17E17E17E17E17E17EA`

Read `ARTICLE.md` for analysis and limitations. `data/` contains the 48 supplied unlock timestamps, three funding observations and contract reads.

## Reproduction status

The initial evidence was gathered through explorer UI reads and screenshots. No raw block-pinned JSON-RPC responses were captured then. The script is a read-only starting point for a fresh verification run, not proof that the first-pass findings have already been independently reproduced.

## Run

```bash
python -m pip install -r requirements.txt
python scripts/verify_vesting.py --rpc https://mainnet-rpc.rayls.com --block latest
```

The script uses `eth_chainId`, `eth_getBlockByNumber` and `eth_call`. Save its full output with the chosen block number/hash. Confirm all selectors against the current verified ABI before treating results as publication-grade evidence.

**Scope:** Parfin lock only. It does not verify the separate investor/team vesting arrangement.
