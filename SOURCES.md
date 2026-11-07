# Sources and provenance

## Public references
- Rayls announcement (29 Oct 2026): https://www.rayls.com/blog/rayls-investors-and-team-extend-rls-vesting
- Lock explorer: https://explorer.rayls.com/address/0x1463889D3a5EAAEE3f066d1CF438A8957F7Db98E
- RLS token explorer: https://explorer.rayls.com/address/0x07e17E17E17E17E17E17E17E17E17E17E17E17EA
- Rayls Public Chain reference: https://docs.rayls.com/docs/public-chain-reference

## User-captured explorer evidence
The conversation contains screenshots/read results for source verification; lock getters; token symbol/decimals; owner/admin counts and membership checks; transaction/log history; and three successful incoming RLS transfers. Funding hashes, blocks, times and amounts are transcribed in `data/funding-transactions.csv`.

## Limitations
No raw JSON-RPC response archive or block-pinned snapshot was captured during the first pass. The source snippets were pasted from the verified source UI. The explorer UI displayed `sweep` with an amount input, while the pasted source signature was `sweep()`; this remains unresolved. The RLS token proxy detection must not be confused with the lock contract's own proxy status.
