
def clean_runner_output(runner_output: str) -> str:
    """Clean runner output for easier comparisons in tests"""
    return runner_output.strip().split('Error: ')[-1]

