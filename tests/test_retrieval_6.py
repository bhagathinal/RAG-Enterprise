import sys
import os

# --------------------------------------------------
# Ensure project root is in Python path
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# Imports from project
# --------------------------------------------------
from Source.retrieval_with_access_control_6 import retrieve_with_access_control
from Source.metrics import precision_at_k


def test_hr_leave_query():
    """
    Test retrieval with access control for HR leave policy
    """

    results = retrieve_with_access_control(
        question="How many leave days are allowed?",
        user_role="employee",
        top_k=5
    )

    precision = precision_at_k(
        retrieved_chunks=results,
        expected_sources=["leave_policy.pdf"]
    )

    print("Precision@K:", precision)

    # Optional assertion (keeps it test-friendly)
    assert precision > 0
