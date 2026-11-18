"""
Pytest configuration and fixture definitions.

Provides dependency-injected fixtures for Playwright browser, page contexts,
Page Objects, and native HTTP API clients, with full IDE IntelliSense.
"""
from typing import Generator, Dict, Any
import pytest
from playwright.sync_api import (
    sync_playwright,
    Playwright,
    Browser,
    BrowserContext,
    Page,
    APIRequestContext,
    APIResponse,
)
from pages.login_page import LoginPage
from config import HEADLESS, SLOW_MO, API_BASE_URL


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Initialize Playwright engine once per test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Launch a single Chromium browser process for the entire test session."""
    browser = playwright_instance.chromium.launch(
        headless=HEADLESS,
        slow_mo=SLOW_MO,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Create a completely isolated browser context (cookies, storage) per test."""
    ctx = browser.new_context()
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Provide a fresh page instance for each test."""
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Provide a LoginPage Page Object instance with native IDE type resolution."""
    return LoginPage(page)


@pytest.fixture(scope="session")
def api_client(playwright_instance: Playwright) -> Generator[APIRequestContext, None, None]:
    """Provide a native Playwright HTTP client for API testing."""
    client = playwright_instance.request.new_context(base_url=API_BASE_URL)
    yield client
    client.dispose()


@pytest.fixture(scope="function")
def api_response_holder() -> Dict[str, Any]:
    """Share mutable API response data across Pytest-BDD step definitions."""
    return {}
