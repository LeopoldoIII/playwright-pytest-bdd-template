"""
Pytest-BDD Scenario Runner.

Binds Gherkin scenarios defined in features/smoke.feature to step definitions.
Can be executed directly via:
    pytest tests/test_smoke.py
Or in parallel with multiple workers:
    pytest -n 4
"""
from pytest_bdd import scenarios
# Import all step definitions so Pytest-BDD discovers them during test collection
from tests.step_defs.test_ui_steps import *
from tests.step_defs.test_api_steps import *

# Discover and bind all scenarios in features/smoke.feature
scenarios("../features/smoke.feature")
