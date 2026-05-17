# Physics Auditor

A CLI tool that fact-checks performance claims against fundamental physical and computational limits. Feed it a claim, and it tells you whether the laws of physics agree.

## Audit Types

### BCI Throughput (`bci_throughput`)
Compares a claimed brain-computer interface data rate against the **Shannon-Hartley channel capacity** — the theoretical maximum bits per second for a channel with a given bandwidth and signal-to-noise ratio.

```
C = B * log2(1 + SNR)
```

### Parallel Speedup (`amdahl`)
Compares a claimed parallel speedup against **Amdahl's Law** — the hard ceiling on speedup given the fraction of work that can actually be parallelized.

```
S_max = 1 / (1 - p)
```

### LLM Inference Bandwidth (`llm_bandwidth`)
Compares a claimed token generation rate against the **memory bandwidth ceiling** — the maximum tokens/sec achievable when every forward pass must read all model weights from VRAM.

```
max_tokens/sec = VRAM_bandwidth / (params * precision_bytes)
```

## Verdicts

Every audit returns one of three verdicts:

| Verdict | Meaning |
|---|---|
| **PLAUSIBLE** | Claim is at or under the theoretical limit |
| **HIGHLY IMPROBABLE** | Claim exceeds the limit but is within 2x |
| **DEFIES PHYSICS/COMPUTE LIMITS** | Claim exceeds 2x the theoretical limit |

## Usage

```bash
# BCI throughput: "Can a 100 Hz, SNR=10 channel carry 1000 bps?"
python3 auditor.py --type bci_throughput --claim 1000 --bandwidth 100 --snr 10

# Amdahl's Law: "Can we get 50x speedup with 95% parallel code?"
python3 auditor.py --type amdahl --claim 50 --parallel-fraction 0.95

# LLM bandwidth: "Can a 70B model generate 100 tokens/sec?"
python3 auditor.py --type llm_bandwidth --claim 100 --model-params 70

# LLM bandwidth with custom hardware params
python3 auditor.py --type llm_bandwidth --claim 100 --model-params 70 \
  --precision-bytes 4 --vram-bandwidth 2.0
```

Example output:

```
Claim:   1000.00 bps
Limit:   345.94 bps (Shannon-Hartley)
Verdict: DEFIES PHYSICS/COMPUTE LIMITS
```

## Tests

```bash
python3 -m pytest tests/ -v
```

## Requirements

Python 3. No external libraries (stdlib only, pytest for tests).
