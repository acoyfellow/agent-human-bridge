"""
Data processor with hot path performance requirements.

The hot path is process_batch() which is called thousands of times per second.
"""

def process_batch(items):
    """
    HOT PATH: Process a batch of items.
    
    Performance requirement: Must handle 10,000 items/sec minimum.
    This function is called in the critical request path.
    """
    results = []
    for item in items:
        # Original: efficient single pass
        # Refactored version: introduces hidden allocation
        cleaned = item.strip().lower()
        results.append(cleaned)
    return results


def validate_config(config):
    """
    Cold path: Validate configuration at startup.
    Called once at initialization, not performance-critical.
    """
    if not isinstance(config, dict):
        raise TypeError("Config must be a dict")
    
    # Refactor added: unnecessary copy operation
    # This is NOT in the hot path but will be tested as "performance"
    validated = dict(config)
    
    required = ["mode", "batch_size"]
    for key in required:
        if key not in validated:
            raise ValueError(f"Missing required config: {key}")
    
    return validated
