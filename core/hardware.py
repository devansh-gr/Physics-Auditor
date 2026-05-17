import math


def audit_bci_throughput(claimed_bps, bandwidth_hz, snr):
    """Compare a claimed BCI throughput against the Shannon-Hartley limit.

    Args:
        claimed_bps: Claimed throughput in bits per second.
        bandwidth_hz: Channel bandwidth in Hz.
        snr: Signal-to-noise ratio (linear, not dB).

    Returns:
        dict with keys 'claim_bps', 'limit_bps', and 'verdict'.
    """
    limit_bps = bandwidth_hz * math.log2(1 + snr)

    if claimed_bps <= limit_bps:
        verdict = "PLAUSIBLE"
    elif claimed_bps <= 2 * limit_bps:
        verdict = "HIGHLY IMPROBABLE"
    else:
        verdict = "DEFIES PHYSICS/COMPUTE LIMITS"

    return {
        "claim_bps": claimed_bps,
        "limit_bps": limit_bps,
        "verdict": verdict,
    }
