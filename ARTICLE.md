# Inside Rayls' 1.07 Billion RLS Lock: An On-Chain Investigation of Parfin's Vesting Contract

**Research status:** explorer-based first-pass verification  
**Research snapshot:** 6 November 2026  
**Network:** Rayls Public Chain  
**Lock contract:** `0x1463889D3a5EAAEE3f066d1CF438A8957F7Db98E`

## Executive summary

This investigation examines the Parfin RLS lock contract referenced in Rayls' token-vesting announcements. The explorer displayed the contract name `RlsTokenLock` and exact-match source verification. Read-only explorer calls reported `actualBalance`, `expectedBalance` and `totalAmount` as the same raw value: `1070493535000000000000000000`. The RLS token contract reported 18 decimals, making that value 1,070,493,535 RLS.

The explorer showed three successful incoming transfers—10, 500,000,000 and 570,493,525 RLS—which sum exactly to 1,070,493,535 RLS. The lock contract reported 48 unlock timestamps. The first converts to 1 December 2027, 00:00 UTC; the final supplied timestamp converts to 1 November 2031, 00:00 UTC. The supplied timestamps are monthly, on the first day of each month.

At the time of inspection, the explorer reads showed `claimable = 0`, `totalClaimed = 0`, `totalBurned = 0`, `tranchesClaimed = 0` and `isFullyFunded = true`. The Token transfers view showed the three incoming transfers and no outgoing transfer in the displayed history.

The source snippets inspected show that `claim()` is restricted to administrators and transfers the claim amount to `msg.sender`; `burn()` is also administrator-only and reduces the schedule basis; and the pasted `sweep()` implementation is administrator-only and checks that `outstanding()` is zero before transferring the remaining balance to the caller. A discrepancy remains: the explorer UI showed `sweep` with an `amount` input, while the pasted verified-source snippet declares `sweep()` without arguments. This must be resolved against the deployed ABI before publication.

This report concerns **the Parfin lock contract only**. It does not verify the separate investor/team vesting arrangement or prove who beneficially controls the sender, owner or administrator addresses.

## 1. Scope and sources

Rayls' 29 October 2026 announcement described revised investor/team vesting and referred to Parfin's separate lock-up extension. These arrangements must not be conflated. This investigation focuses on the Parfin lock contract at the address above.

Primary references:
- Rayls announcement: https://www.rayls.com/blog/rayls-investors-and-team-extend-rls-vesting
- Lock contract: https://explorer.rayls.com/address/0x1463889D3a5EAAEE3f066d1CF438A8957F7Db98E
- RLS token: https://explorer.rayls.com/address/0x07e17E17E17E17E17E17E17E17E17E17E17E17E17EA
- Rayls Public Chain reference: https://docs.rayls.com/docs/public-chain-reference

## 2. Methodology and evidence standard

The first pass used the explorer's verified-source page, Read/Write interface, Logs, Transactions and Token transfers views, plus source snippets inspected during the session. Figures in the CSV files are transcribed from those explorer observations.

Evidence distinctions:
- **Explorer observation:** displayed value, event or transaction.
- **Source-code observation:** behavior visible in the pasted verified-source snippet.
- **Calculation:** arithmetic or timestamp conversion from observed values.

**Reproducibility limitation:** no raw JSON-RPC responses or block-pinned snapshot were saved during the first pass. The included script is a starting point for a fresh read-only reproduction; it does not mean those RPC checks have already been executed. A publication-grade follow-up should save each request/response and the block number, hash and timestamp.

## 3. Contract and token

The explorer identified the lock as `RlsTokenLock` and showed exact-match source verification. The inspected declaration was `contract RlsTokenLock is ReentrancyGuard`. The lock's `token()` getter returned `0x07e17E17E17E17E17E17E17E17E17E17E17E17EA`; the token explorer reads returned symbol `RLS` and decimals `18`.

The RLS token contract was separately detected by the explorer as an EIP-1967 Transparent Proxy. That observation concerns the **token**, not the lock. The lock source inspected did not show common upgrade-framework identifiers, but the lock's EIP-1967 implementation/admin storage slots were not checked. Therefore this report does not make a definitive claim that the lock is non-upgradeable.

## 4. Funding reconciliation

The explorer displayed three successful incoming transfers from `0xab5309BE3d6E228288DA1F68dF3F993A550dEC7c`:

| Amount | Block | Time (UTC+05:30) |
|---:|---:|---|
| 10 RLS | 6,430,716 | 6 Aug 2026, 17:16:47 |
| 500,000,000 RLS | 6,430,829 | 6 Aug 2026, 17:19:11 |
| 570,493,525 RLS | 6,430,872 | 6 Aug 2026, 17:20:07 |
| **1,070,493,535 RLS** | | |

The sum exactly matches the three raw balance/configuration reads after applying 18 decimals. The explorer's Token transfers tab showed these three incoming transfers and no outgoing transfer in the history displayed at inspection time. A fresh full-range Transfer-log query is still needed to independently verify completeness.

## 5. Unlock schedule

`trancheCount()` returned 48. `unlockTimes()` returned the 48 timestamps in `data/unlock-schedule.csv`. The first is 1 December 2027, 00:00 UTC; the final is 1 November 2031, 00:00 UTC. The timestamps are consecutive calendar months on day one.

`unlockedTranches(timestamp)` returned 1 for the first timestamp, 2 for the second, and 48 for the final timestamp. It returns a count of unlocked tranches, not an RLS amount.

## 6. Vesting and claim mechanics

The inspected snippets define:

```solidity
function scheduleBasis() public view returns (uint256) {
    return totalAmount - totalBurned;
}
function outstanding() public view returns (uint256) {
    return scheduleBasis() - totalClaimed;
}
```

Thus, based on the inspected source, `outstanding = totalAmount - totalBurned - totalClaimed`.

The inspected `claimable()` function calculates due amounts from unlocked tranches, already-claimed tranches and the remaining outstanding balance. Before the final date it uses integer division: `(unlocked - tranchesClaimed) * (owed / remaining)`. At or after the final tranche it returns the full outstanding amount. This is dynamic against the remaining balance, not necessarily a fixed 1/48 of the original amount each time; Solidity integer division rounds down at intermediate calculations.

The inspected `claim()` is `external nonReentrant onlyAdmin`. It checks the first unlock date, calculates claimable value, applies funding checks, updates counters and calls `_transferOut(msg.sender, amount)`. Thus the contract transfers the claim to the calling administrator. The inspected function does not itself demonstrate subsequent distribution to individual beneficiaries.

## 7. Burn, sweep and administrative controls

The inspected `burn(uint256 amount)` is administrator-only. It checks full funding, prevents burning more than `outstanding()`, increments `totalBurned`, emits an event and calls the token's burn function. Since `scheduleBasis()` subtracts `totalBurned`, burns reduce the schedule basis.

The pasted source for `sweep()` has no argument and checks `outstanding() == 0` before transferring the remaining token balance to `msg.sender`. However, the explorer UI displayed a `sweep` method with an `amount` input. **This source/ABI signature discrepancy is unresolved.** Do not publish a definitive description of the deployed sweep interface until the verified ABI and runtime bytecode are checked.

The inspected `onlyAdmin` modifier checks `_admins[msg.sender]`. The explorer reported three owners and five administrators; the candidate addresses were individually tested using `isOwner()`/`isAdmin()` and returned true. A historically removed owner address returned false. These role checks do not identify the real-world people or organizations controlling the addresses.

## 8. State at inspection

Explorer reads showed:
- `isFullyFunded = true`;
- `claimable = 0`;
- `totalBurned = 0`;
- `totalClaimed = 0`;
- `tranchesClaimed = 0`;
- `trancheCount = 48`.

These values are consistent with the full configured allocation remaining funded and no claims or burns having been recorded through the inspected contract methods at that time.

## 9. Limitations

This first pass does not establish:
- beneficial ownership or real-world identity of any address;
- whether administrators distribute claimed tokens to intended beneficiaries;
- the separate investor/team vesting arrangement;
- the lock's definitive proxy/non-proxy status;
- the resolution of the `sweep()` signature discrepancy;
- a complete independently queried event/transfer history at a pinned block;
- independent reproduction from saved raw RPC responses.

The next pass should query the Rayls RPC at a fixed block tag, save raw responses, verify the lock's EIP-1967 slots, compare deployed ABI and source, and reconcile all ERC-20 Transfer logs through that block.

## 10. Conclusion

The explorer evidence supports a scoped conclusion: the Parfin `RlsTokenLock` is configured for 1,070,493,535 RLS; three displayed incoming transfers sum exactly to that amount; the contract reports a fully funded state; and it stores 48 monthly unlock timestamps from December 2027 through November 2031. At inspection, reads showed no claims, burns or claimed tranches.

The inspected source snippets indicate that claims are administrator-triggered and paid to the calling administrator, that administrators can burn outstanding tokens subject to checks, and that the pasted sweep implementation restricts sweeping until settlement. The administrator-controlled claim and subsequent distribution process is therefore an important part of the trust model.

These findings verify the visible configuration and explorer-reported state of the **Parfin lock contract**. They do not verify the separate investor/team schedule or prove downstream distribution. A block-pinned RPC evidence pass remains necessary for a fully reproducible publication.
