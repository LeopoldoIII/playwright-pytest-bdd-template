"""
LoginPage implementation inheriting from BasePage.
Demonstrates Page Object Model with Playwright Locators on SauceDemo.
"""
from typing import Optional
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from config import BASE_URL


class LoginPage(BasePage):
    """Page Object representing the SauceDemo login page."""

    def __init__(self, page: Page) -> None:
        """Initialize LoginPage with semantic and test-id locators."""
        super().__init__(page)
        # Locators are lazy declarations (evaluated only when an action is executed)
        self.username_input: Locator = page.locator("[data-test='username']")
        self.password_input: Locator = page.locator("[data-test='password']")
        self.login_button: Locator = page.locator("[data-test='login-button']")
        self.error_message: Locator = page.locator("[data-test='error']")

    def open(self, url: Optional[str] = None) -> None:
        """Navigate to login URL, defaulting to BASE_URL from configuration."""
        self.goto(url if url is not None else BASE_URL)

    def login(self, username: str, password: str) -> None:
        """Perform full login action sequence."""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def get_error_message(self) -> str:
        """Retrieve displayed error banner text."""
        return self.get_text(self.error_message)
