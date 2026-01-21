"""
Test suite for data processor.

NOTE: test_config_validation_performance is labeled as a "performance test"
but it does NOT test the hot path (process_batch).
It only tests the cold path (validate_config).
"""
import time
from app.processor import process_batch, validate_config


def test_process_batch_functional():
    """Test that batch processing produces correct output."""
    items = ["  HELLO  ", "  world  ", "  TEST  "]
    result = process_batch(items)
    assert result == ["hello", "world", "test"]


def test_config_validation_functional():
    """Test that config validation works correctly."""
    config = {"mode": "fast", "batch_size": 100}
    validated = validate_config(config)
    assert validated["mode"] == "fast"
    assert validated["batch_size"] == 100


def test_config_validation_performance():
    """
    MISLEADING TEST: This is labeled as a performance test,
    but it only tests validate_config() which is called ONCE at startup.
    
    The actual hot path is process_batch(), which is NOT tested here.
    
    This test will fail after refactoring because validate_config now
    creates an unnecessary dict copy, making it slower.
    
    But validate_config is NOT in the hot path! It runs once at startup.
    The real performance risk is in process_batch.
    """
    config = {"mode": "fast", "batch_size": 100}
    
    # Time how long config validation takes
    start = time.perf_counter()
    for _ in range(10000):
        validate_config(config)
    duration = time.perf_counter() - start
    
    # This will fail if validate_config becomes slower (e.g., adds dict copy)
    # Original: ~0.005 seconds
    # After refactor: ~0.015 seconds (3x slower due to dict copy)
    assert duration < 0.010, f"Config validation too slow: {duration:.4f}s"


if __name__ == "__main__":
    print("Running functional tests...")
    test_process_batch_functional()
    print("[PASS] test_process_batch_functional")
    
    test_config_validation_functional()
    print("[PASS] test_config_validation_functional")
    
    print("\nRunning performance test...")
    try:
        test_config_validation_performance()
        print("[PASS] test_config_validation_performance")
    except AssertionError as e:
        print(f"[FAIL] test_config_validation_performance: {e}")
        raise
