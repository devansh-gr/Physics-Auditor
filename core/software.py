def _verdict(claimed, limit):
    if claimed <= limit:
        return "PLAUSIBLE"
    elif claimed <= 2 * limit:
        return "HIGHLY IMPROBABLE"
    else:
        return "DEFIES PHYSICS/COMPUTE LIMITS"


def audit_amdahl(claimed_speedup, parallel_fraction):
    """Compare a claimed speedup against Amdahl's Law maximum.

    Args:
        claimed_speedup: The claimed parallel speedup factor.
        parallel_fraction: Fraction of work that is parallelizable (0 to 1).

    Returns:
        dict with keys 'claim_speedup', 'limit_speedup', and 'verdict'.
    """
    limit_speedup = 1 / (1 - parallel_fraction)
    return {
        "claim_speedup": claimed_speedup,
        "limit_speedup": limit_speedup,
        "verdict": _verdict(claimed_speedup, limit_speedup),
    }


def audit_llm_bandwidth(claimed_tokens_per_sec, model_params_billions,
                         precision_bytes=2, vram_bandwidth_TBs=3.35):
    """Compare claimed token generation rate against the memory bandwidth ceiling.

    Args:
        claimed_tokens_per_sec: Claimed inference throughput in tokens/sec.
        model_params_billions: Model size in billions of parameters.
        precision_bytes: Bytes per parameter (e.g. 2 for FP16).
        vram_bandwidth_TBs: VRAM bandwidth in terabytes per second.

    Returns:
        dict with keys 'claim_tps', 'limit_tps', and 'verdict'.
    """
    limit_tps = (vram_bandwidth_TBs * 1e12) / (model_params_billions * 1e9 * precision_bytes)
    return {
        "claim_tps": claimed_tokens_per_sec,
        "limit_tps": limit_tps,
        "verdict": _verdict(claimed_tokens_per_sec, limit_tps),
    }
