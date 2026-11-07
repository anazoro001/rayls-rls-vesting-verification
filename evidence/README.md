# Evidence capture checklist

For a publication-grade second pass, save:
1. `eth_chainId` result.
2. `eth_getBlockByNumber` response with block number, hash and timestamp.
3. Every `eth_call` raw request/response at the same fixed block tag.
4. Full ERC-20 Transfer log query from contract creation through snapshot block.
5. Lock contract EIP-1967 implementation/admin storage-slot reads.
6. Deployed ABI entries for `sweep` and bytecode/source comparison.

The current first-pass package contains explorer observations only; it does not include these raw RPC captures.
