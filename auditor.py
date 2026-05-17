import argparse

from core.hardware import audit_bci_throughput
from core.software import audit_amdahl, audit_llm_bandwidth


def main():
    parser = argparse.ArgumentParser(description="Physics Auditor CLI")
    parser.add_argument("--type", required=True,
                        choices=["bci_throughput", "amdahl", "llm_bandwidth"],
                        help="Type of audit to run")
    parser.add_argument("--claim", required=True, type=float,
                        help="Claimed value")
    parser.add_argument("--bandwidth", type=float,
                        help="Channel bandwidth in Hz (bci_throughput)")
    parser.add_argument("--snr", type=float,
                        help="Signal-to-noise ratio, linear (bci_throughput)")
    parser.add_argument("--parallel-fraction", type=float,
                        help="Fraction of parallelizable work, 0-1 (amdahl)")
    parser.add_argument("--model-params", type=float,
                        help="Model size in billions of parameters (llm_bandwidth)")
    parser.add_argument("--precision-bytes", type=float, default=2,
                        help="Bytes per parameter (llm_bandwidth, default: 2)")
    parser.add_argument("--vram-bandwidth", type=float, default=3.35,
                        help="VRAM bandwidth in TB/s (llm_bandwidth, default: 3.35)")
    args = parser.parse_args()

    def require(*flags):
        missing = [f for f in flags if getattr(args, f.replace("-", "_")) is None]
        if missing:
            parser.error(f"--type {args.type} requires: " +
                         ", ".join(f"--{f}" for f in missing))

    if args.type == "bci_throughput":
        require("bandwidth", "snr")
        result = audit_bci_throughput(args.claim, args.bandwidth, args.snr)
        print(f"Claim:   {result['claim_bps']:.2f} bps")
        print(f"Limit:   {result['limit_bps']:.2f} bps (Shannon-Hartley)")
        print(f"Verdict: {result['verdict']}")

    elif args.type == "amdahl":
        require("parallel-fraction")
        result = audit_amdahl(args.claim, args.parallel_fraction)
        print(f"Claim:   {result['claim_speedup']:.2f}x speedup")
        print(f"Limit:   {result['limit_speedup']:.2f}x speedup (Amdahl's Law)")
        print(f"Verdict: {result['verdict']}")

    elif args.type == "llm_bandwidth":
        require("model-params")
        result = audit_llm_bandwidth(args.claim, args.model_params,
                                     args.precision_bytes, args.vram_bandwidth)
        print(f"Claim:   {result['claim_tps']:.2f} tokens/sec")
        print(f"Limit:   {result['limit_tps']:.2f} tokens/sec (memory bandwidth ceiling)")
        print(f"Verdict: {result['verdict']}")


if __name__ == "__main__":
    main()
