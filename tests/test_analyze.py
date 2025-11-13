import pytest
from smartrca.analyze import analyze_text_log

def test_analyze_text_basic():
    sample_input = "Error: job failed due to timeout"
    response = analyze_text_log(sample_input)
    assert response is not None



