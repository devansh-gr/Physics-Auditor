from core.software import audit_amdahl, audit_llm_bandwidth


class TestAuditAmdahl:

    def test_plausible_under_limit(self):
        # parallel_fraction=0.9 -> max speedup = 10
        result = audit_amdahl(5, 0.9)
        assert result["verdict"] == "PLAUSIBLE"
        assert result["claim_speedup"] == 5

    def test_plausible_exactly_at_limit(self):
        limit = 1 / (1 - 0.9)
        result = audit_amdahl(limit, 0.9)
        assert result["verdict"] == "PLAUSIBLE"
        assert result["limit_speedup"] == limit

    def test_highly_improbable(self):
        # claim 15x with max 10x -> between 1x and 2x limit
        result = audit_amdahl(15, 0.9)
        assert result["verdict"] == "HIGHLY IMPROBABLE"

    def test_highly_improbable_at_double(self):
        result = audit_amdahl(20, 0.9)
        assert result["verdict"] == "HIGHLY IMPROBABLE"

    def test_defies_physics(self):
        result = audit_amdahl(20.01, 0.9)
        assert result["verdict"] == "DEFIES PHYSICS/COMPUTE LIMITS"

    def test_limit_calculation(self):
        # parallel_fraction=0.5 -> max speedup = 2
        result = audit_amdahl(1, 0.5)
        assert result["limit_speedup"] == 2.0

    def test_return_keys(self):
        result = audit_amdahl(1, 0.5)
        assert set(result.keys()) == {"claim_speedup", "limit_speedup", "verdict"}


class TestAuditLlmBandwidth:

    def _limit(self, params_b, precision=2, vram_bw=3.35):
        return (vram_bw * 1e12) / (params_b * 1e9 * precision)

    def test_plausible_under_limit(self):
        result = audit_llm_bandwidth(10, 70)
        assert result["verdict"] == "PLAUSIBLE"
        assert result["claim_tps"] == 10

    def test_plausible_exactly_at_limit(self):
        limit = self._limit(70)
        result = audit_llm_bandwidth(limit, 70)
        assert result["verdict"] == "PLAUSIBLE"

    def test_highly_improbable(self):
        limit = self._limit(70)
        result = audit_llm_bandwidth(limit + 1, 70)
        assert result["verdict"] == "HIGHLY IMPROBABLE"

    def test_highly_improbable_at_double(self):
        limit = self._limit(70)
        result = audit_llm_bandwidth(2 * limit, 70)
        assert result["verdict"] == "HIGHLY IMPROBABLE"

    def test_defies_physics(self):
        limit = self._limit(70)
        result = audit_llm_bandwidth(2 * limit + 0.01, 70)
        assert result["verdict"] == "DEFIES PHYSICS/COMPUTE LIMITS"

    def test_custom_precision_and_vram(self):
        result = audit_llm_bandwidth(10, 7, precision_bytes=4, vram_bandwidth_TBs=2.0)
        expected_limit = (2.0 * 1e12) / (7 * 1e9 * 4)
        assert result["limit_tps"] == expected_limit

    def test_return_keys(self):
        result = audit_llm_bandwidth(10, 70)
        assert set(result.keys()) == {"claim_tps", "limit_tps", "verdict"}
