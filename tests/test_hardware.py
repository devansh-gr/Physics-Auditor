import math

from core.hardware import audit_bci_throughput


def _shannon_limit(bandwidth, snr):
    return bandwidth * math.log2(1 + snr)


class TestAuditBciThroughput:

    def test_plausible_under_limit(self):
        result = audit_bci_throughput(100, 100, 10)
        assert result["verdict"] == "PLAUSIBLE"
        assert result["claim_bps"] == 100

    def test_plausible_exactly_at_limit(self):
        limit = _shannon_limit(100, 10)
        result = audit_bci_throughput(limit, 100, 10)
        assert result["verdict"] == "PLAUSIBLE"

    def test_highly_improbable_just_over_limit(self):
        limit = _shannon_limit(100, 10)
        result = audit_bci_throughput(limit + 0.01, 100, 10)
        assert result["verdict"] == "HIGHLY IMPROBABLE"

    def test_highly_improbable_at_double_limit(self):
        limit = _shannon_limit(100, 10)
        result = audit_bci_throughput(2 * limit, 100, 10)
        assert result["verdict"] == "HIGHLY IMPROBABLE"

    def test_defies_physics_over_double(self):
        limit = _shannon_limit(100, 10)
        result = audit_bci_throughput(2 * limit + 0.01, 100, 10)
        assert result["verdict"] == "DEFIES PHYSICS/COMPUTE LIMITS"

    def test_limit_calculation_matches_shannon_hartley(self):
        result = audit_bci_throughput(0, 200, 15)
        expected = 200 * math.log2(1 + 15)
        assert result["limit_bps"] == expected

    def test_return_keys(self):
        result = audit_bci_throughput(50, 100, 5)
        assert set(result.keys()) == {"claim_bps", "limit_bps", "verdict"}

    def test_zero_snr(self):
        result = audit_bci_throughput(0, 100, 0)
        assert result["limit_bps"] == 0.0
        assert result["verdict"] == "PLAUSIBLE"

    def test_high_bandwidth_low_snr(self):
        result = audit_bci_throughput(1, 10000, 0.001)
        assert result["verdict"] == "PLAUSIBLE"
        assert result["limit_bps"] > 0

    def test_claim_echoed_back(self):
        result = audit_bci_throughput(42.5, 100, 10)
        assert result["claim_bps"] == 42.5
