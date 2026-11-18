"""
UI step definitions for Pytest-BDD.

Page objects and browser pages are received directly as injected fixtures
(login_page, page) with 100% native IDE autocompletion and type safety.
"""
import re
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


# ==========================================
# UI Step Definitions
# ==========================================

@given('the user navigates to the login page')
def step_navigate_login(login_page: LoginPage) -> None:
    """Navigate to the target login page."""
    login_page.open()


@when(parsers.parse('the user logs in with username "{username}" and password "{password}"'))
def step_login_credentials(login_page: LoginPage, username: str, password: str) -> None:
    """Submit credentials on the login page."""
    login_page.login(username, password)


@then('the user should see the inventory page header')
def step_verify_inventory_page(page: Page) -> None:
    """Verify redirection to inventory and visible products title."""
    expect(page).to_have_url(re.compile(r".*inventory\.html"))
    header = page.locator(".title")
    expect(header).to_be_visible()
    expect(header).to_have_text("Products")


@then(parsers.parse('the user should see the error message "{expected_message}"'))
def step_verify_login_error(login_page: LoginPage, expected_message: str) -> None:
    """Verify error banner visibility and text content."""
    error_banner = login_page.error_message
    expect(error_banner).to_be_visible()
    expect(error_banner).to_contain_text(expected_message)
