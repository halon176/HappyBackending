import pytest

if __name__ == "__main__":
    pytest.main(["-v", "tests/", "--asyncio-mode=auto", "--disable-warnings"])