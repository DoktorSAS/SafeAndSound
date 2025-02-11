import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

import utils.Ciphers as Ciphers
from utils.Enum import CryptoType

def check_values(expected_values, actual_values):
    """
    Check if the given values match the expected values and report the results.

    :param expected_values: A dictionary where keys are identifiers and values are expected results.
    :param actual_values: A dictionary with the same keys as expected_values but with actual results.
    :return: None, prints the results in the specified format.
    """
    # List to store failed checks
    failed_checks = []
    
    # Check each value
    for key, expected in expected_values.items():
        actual = actual_values.get(key, None)
        if actual != expected:
            failed_checks.append((key, expected, actual))
            # Generate an error for each failed check
            print(f"Error: Check for '{key}' failed. Expected: {expected}, Got: {actual}", file=sys.stderr)
    
    # Print results in the specified format
    for key, expected in expected_values.items():
        actual = actual_values.get(key, None)
        status = "✅" if expected == actual else "❌"
        print(f"[{status}] {key}:")
        print(f"\t{expected} = {actual if actual is not None else 'None'}")
    
    # If there were any failures, print a summary
    if failed_checks:
        print("\nSummary of Failures:")
        for fail in failed_checks:
            print(f"- {fail[0]}: Expected {fail[1]}, but got {fail[2]}")

if __name__ == "__main__":
    actual_values = {
        'Base64_encode': Ciphers.encrypt("Hello, World!", CryptoType.BASE64, ""),
        'Base64_decode': Ciphers.decrypt('SGVsbG8sIFdvcmxkIQ==', CryptoType.BASE64, ""),
    }

    expected_values = {
        'Base64_encode': b'SGVsbG8sIFdvcmxkIQ==',
        'Base64_decode': b"Hello, World!",
    }

    check_values(expected_values, actual_values)