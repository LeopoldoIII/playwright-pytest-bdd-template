# Antigravity AI Project Rules & Guidelines (Pytest-BDD)

## 1. Universal Language Requirement
- **All code, docstrings, comments, test descriptions, Gherkin scenarios, and technical documentation MUST be written strictly in English.**
- When interacting with the user, respond in the user's preferred language, but ensure that all repository assets (code, git messages, docs) remain 100% in English.

---

## 2. Core Python, Pytest & Playwright Standards

### Page Object Model (Clean POM)
- **Separation of Concerns**: Page Objects in `pages/` represent UI state, locators, and user interactions.
- **NO Assertions in Page Objects**: Do not import or execute `expect(...)` inside Page Objects. Assertions belong strictly in step definitions (`tests/step_defs/`).
- **Inheritance**: All Page Objects must inherit from `BasePage` (`pages.base_page.BasePage`).
- **Locators**: Use `page.locator(...)` or semantic locators (`page.get_by_role`, `page.get_by_label`, `page.get_by_test_id`). Locators are lazy; declare them in `__init__`.

### Fixtures & State Management (No Dynamic Context)
- **Use Pytest Fixtures**: Never create a dynamic `context` bag or mutable global state.
- **Dependency Injection**: Inject Page Objects (`login_page`), pages (`page`), and API clients (`api_client`) directly into step definition functions as fixture arguments.
- **IDE Navigation**: Because step functions declare typed fixture arguments (`login_page: LoginPage`), "Go to Definition" (F12 / Cmd+Click) and IntelliSense work natively without any helper type files.

### Web-First Assertions
- In step definitions, always prefer Playwright's web-first assertions (`expect(locator).to_be_visible()`, `expect(locator).to_have_text(...)`, `expect(page).to_have_url(...)`).
- Do NOT use manual polling, `time.sleep()`, or raw Python `assert locator.inner_text() == ...` for UI states, as Playwright's auto-waiting handles stability automatically.

### Parallel Execution with `pytest-xdist`
- Design tests and fixtures to be strictly independent and isolated.
- Run tests concurrently across CPU cores via `pytest -n auto` or `pytest -n 4`.

### Centralized Configuration
- Never hardcode URLs, credentials, timeouts, or execution flags.
- Always import settings from `config.py` (e.g. `BASE_URL`, `API_BASE_URL`, `STANDARD_USER`, `SECRET_PASSWORD`, `DEFAULT_TIMEOUT`, `HEADLESS`, `SLOW_MO`).
- Any new environment variable must be defined in `config.py`, `.env`, and `.env.example`.
