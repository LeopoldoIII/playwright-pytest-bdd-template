"""
API step definitions for Pytest-BDD using native Playwright HTTP client.
"""
from typing import Dict, Any
from pytest_bdd import when, then, parsers
from playwright.sync_api import APIRequestContext


# ==========================================
# API Step Definitions
# ==========================================

@when(parsers.parse('the user requests API details for user "{user_id}"'))
def step_api_get_user(
    api_client: APIRequestContext, api_response_holder: Dict[str, Any], user_id: str
) -> None:
    """Execute GET request using Playwright's native HTTP context."""
    res = api_client.get(f"/users/{user_id}")
    api_response_holder["response"] = res


@when(
    parsers.parse(
        'the user creates a new user with firstName "{first_name}" and lastName "{last_name}"'
    )
)
def step_api_create_user(
    api_client: APIRequestContext,
    api_response_holder: Dict[str, Any],
    first_name: str,
    last_name: str,
) -> None:
    """Execute POST request with JSON payload using Playwright's native HTTP context."""
    payload = {"firstName": first_name, "lastName": last_name}
    res = api_client.post(
        "/users/add",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    api_response_holder["response"] = res


@then(parsers.parse('the API response status code should be {status_code:d}'))
def step_verify_api_status(
    api_response_holder: Dict[str, Any], status_code: int
) -> None:
    """Verify HTTP response status code."""
    res = api_response_holder["response"]
    assert res.status == status_code, (
        f"Expected HTTP status {status_code}, but got {res.status}."
    )


@then(parsers.parse('the response body should contain username "{expected_username}"'))
def step_verify_api_username(
    api_response_holder: Dict[str, Any], expected_username: str
) -> None:
    """Verify username attribute in the response body."""
    res = api_response_holder["response"]
    data = res.json()
    actual_username = data.get("username")
    assert actual_username == expected_username, (
        f"Expected username '{expected_username}', got '{actual_username}'."
    )


@then(parsers.parse('the response body should contain firstName "{expected_first_name}"'))
def step_verify_api_firstname(
    api_response_holder: Dict[str, Any], expected_first_name: str
) -> None:
    """Verify firstName attribute in the response body."""
    res = api_response_holder["response"]
    data = res.json()
    actual_name = data.get("firstName")
    assert actual_name == expected_first_name, (
        f"Expected firstName '{expected_first_name}', got '{actual_name}'."
    )
