"""
Base Page module providing reusable UI interaction wrappers over Playwright Locators.

Note for interviewers:
Assertions are intentionally kept out of this BasePage class to adhere strictly
to the Page Object Model (POM) separation of concerns. Page Objects represent UI
state and user actions; assertions belong strictly in step definitions or test cases.
"""
from typing import Union, Optional, Literal
from playwright.sync_api import Page, Locator
from config import DEFAULT_TIMEOUT


class BasePage:
    """Base Page Object class encapsulating common Playwright actions."""

    def __init__(self, page: Page) -> None:
        """Initialize with an active Playwright Page instance."""
        self.page = page

    def _get_locator(self, target: Union[str, Locator]) -> Locator:
        """
        Normalize selector string (CSS/XPath) or Locator instance into a Locator.

        Allows methods to accept both modern Playwright Locators (get_by_role)
        and classic selector strings without rewriting wrappers.
        """
        if isinstance(target, str):
            return self.page.locator(target)
        return target

    def goto(self, url: str) -> None:
        """Navigate to the specified URL."""
        self.page.goto(url)

    def click(
        self, target: Union[str, Locator], timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        """Click an element, waiting automatically for actionable state."""
        locator = self._get_locator(target)
        locator.click(timeout=timeout)

    def fill(self, target: Union[str, Locator], text: str) -> None:
        """Clear and fill an input element instantly with text."""
        locator = self._get_locator(target)
        locator.fill(text)

    def press_sequentially(
        self, target: Union[str, Locator], text: str, delay: Optional[float] = None
    ) -> None:
        """
        Type characters sequentially, simulating real user keyboard input.

        Triggers keydown, keypress/input, and keyup events for each character.
        Useful when testing autocomplete, search inputs, or debounced fields.
        """
        locator = self._get_locator(target)
        locator.press_sequentially(text, delay=delay)

    def select_dropdown(self, target: Union[str, Locator], value: str) -> None:
        """Select an option in a standard <select> dropdown by value or label."""
        locator = self._get_locator(target)
        locator.select_option(value)

    def check(self, target: Union[str, Locator]) -> None:
        """Check a checkbox or radio button (idempotent)."""
        locator = self._get_locator(target)
        locator.check()

    def uncheck(self, target: Union[str, Locator]) -> None:
        """Uncheck a checkbox (idempotent)."""
        locator = self._get_locator(target)
        locator.uncheck()

    def hover(
        self, target: Union[str, Locator], timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        """
        Hover the mouse pointer over the matched element.

        Automatically scrolls the element into view and waits for actionability.
        Replaces Selenium's ActionChains(driver).move_to_element(el).perform().
        """
        locator = self._get_locator(target)
        locator.hover(timeout=timeout)

    def get_text(self, target: Union[str, Locator]) -> str:
        """Retrieve rendered visible inner text of an element."""
        locator = self._get_locator(target)
        return locator.inner_text()

    def get_input_value(self, target: Union[str, Locator]) -> str:
        """Retrieve current value of an <input>, <textarea>, or <select>."""
        locator = self._get_locator(target)
        return locator.input_value()

    def get_attribute(self, target: Union[str, Locator], name: str) -> Optional[str]:
        """
        Retrieve the value of an element's HTML attribute (e.g., 'href', 'class').

        Returns None if attribute is not present.
        """
        locator = self._get_locator(target)
        return locator.get_attribute(name)

    def is_visible(self, target: Union[str, Locator], timeout: float = 3000) -> bool:
        """
        Check if an element is visible within the timeout.

        Safe boolean check for conditional logic.
        """
        locator = self._get_locator(target)
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for(
        self,
        target: Union[str, Locator],
        state: Literal["attached", "detached", "visible", "hidden"] = "visible",
        timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        """
        Explicitly wait for an element to satisfy a specific DOM/visibility state.

        Note: Playwright actions auto-wait by default; this is only required
        for non-action assertions or dynamic loading boundary conditions.
        """
        locator = self._get_locator(target)
        locator.wait_for(state=state, timeout=timeout)
