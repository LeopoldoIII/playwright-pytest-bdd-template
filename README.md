# Minimal Playwright & Pytest-BDD Template (Python)

A production-ready, enterprise BDD test automation template engineered specifically for technical automation interviews, pair-programming sessions, and scalable test suites using **Playwright**, **Pytest-BDD**, **pytest-xdist (Parallel Execution)**, and **Clean Page Object Model**.

---

## 1. Quick Setup (Under 1 Minute)

Run the following commands in your terminal:

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Chromium browser binary
playwright install chromium
```

---

## 2. Test Execution Commands

### Sequential Execution
```bash
# Run all scenarios (UI + API)
pytest

# Run UI scenarios only
pytest -m ui

# Run API scenarios only
pytest -m api

# Run negative scenarios only
pytest -m negative
```

### Parallel Execution (Powered by `pytest-xdist`)
Distribute test execution across multiple CPU worker processes concurrently:
```bash
# Run all tests using 4 parallel workers
pytest -n 4

# Run all tests auto-detecting available CPU cores
pytest -n auto
```

### Headed Mode & Debugging
```bash
# Watch the browser execute visually on your screen
HEADLESS=false pytest -m ui
```

---

## 3. Project Structure

```
playwright-pytest-bdd-template/
├── .env                         # Execution flags and credentials (not committed to VCS)
├── .env.example                 # Template for environment variables
├── config.py                    # Centralized typed configuration loaded via python-dotenv
├── pytest.ini                   # Pytest markers, test paths, and BDD directory config
├── requirements.txt             # playwright, pytest, pytest-bdd, pytest-xdist, python-dotenv
├── .vscode/                     # Autocomplete settings for VS Code
│   ├── settings.json
│   └── extensions.json
├── AGENTS.md                    # Antigravity AI rules and quality standards
├── pages/                       # Page Object Model layer (Clean POM)
│   ├── __init__.py
│   ├── base_page.py             # Action wrappers (click, fill, hover, press_sequentially, wait)
│   └── login_page.py            # SauceDemo LoginPage object
├── features/                    # Gherkin Scenarios
│   └── smoke.feature            # UI & REST API scenarios
└── tests/                       # Pytest test execution layer
    ├── conftest.py              # Injected fixtures (browser, page, login_page, api_client)
    ├── test_smoke.py            # Pytest-BDD Scenario Runner
    └── step_defs/               # Step definitions receiving typed fixtures
        ├── __init__.py
        ├── test_ui_steps.py     # UI step definitions
        └── test_api_steps.py    # API step definitions
```

---

## 4. Key Architectural Comparison: Pytest-BDD vs. Behave

| Dimension | Behave (`playwright-py-template`) | Pytest-BDD (`playwright-pytest-bdd-template`) | Key Technical Difference |
| :--- | :--- | :--- | :--- |
| **Test Runner** | `behave` | `pytest` | Pytest is the industry standard test runner in Python with a vast plugin ecosystem. |
| **State & Lifecycle** | Mutable dynamic `context` (requires `StepContext` typing) | **Dependency Injection via Fixtures (`conftest.py`)** | Fixtures are modular, scoped (`session`, `function`), and automatically clean up resources with `yield`. |
| **Parallel Execution** | No native support (requires brittle shell workarounds) | **Native via `pytest-xdist` (`pytest -n 4`)** | Tests distribute across worker processes seamlessly with isolated browser contexts. |
| **IDE Autocomplete** | Requires declaring attributes in `features/types.py` | **Native out-of-the-box** | Step definition arguments are typed directly: `def step_login(login_page: LoginPage):`. |
| **Official Playwright Tooling** | Manual custom hooks in `environment.py` | Full compatibility with official Microsoft plugins (`pytest-playwright`). | Native video recording, tracing, and multi-browser support. |

---

## 5. Indispensable UI Methods Cheat Sheet: Selenium vs. Playwright (Python)

In Playwright (`sync_api`), you first define the locator (`page.locator(...)` or semantic helpers like `page.get_by_role(...)`) and then execute the action:

| UI Action | Selenium (`webdriver`) | Playwright (`sync_api`) | Key Interview Notes |
| :--- | :--- | :--- | :--- |
| **Navigate to URL** | `driver.get("https://...")` | `page.goto("https://...")` | Playwright waits by default for the `load` event. |
| **Find Element** | `driver.find_element(By.CSS_SELECTOR, "...")` | `page.locator("...")` or `page.get_by_role(...)` | Playwright locators are **lazy** (they do not query the DOM until an action is executed). |
| **Click** | `element.click()` | `locator.click()` | Auto-waits for element to be visible, stable, receive events, and not be covered. |
| **Fill Input** | `element.clear()` + `element.send_keys("abc")` | `locator.fill("abc")` | `.fill()` clears the input and inserts text instantly. To simulate real human typing letter-by-letter, use `locator.press_sequentially("abc")`. |
| **Get Visible Text** | `element.text` | `locator.inner_text()` | `inner_text()` returns only rendered/visible text. `locator.text_content()` returns all node text (equivalent to `textContent`). |
| **Get Input Value** | `element.get_attribute("value")` | `locator.input_value()` | Playwright has a dedicated method exclusively for `<input>`, `<textarea>`, and `<select>` values. |
| **Get Attribute** | `element.get_attribute("href")` | `locator.get_attribute("href")` | Functions identically. |
| **Select Dropdown** | `Select(element).select_by_value("1")` | `locator.select_option("1")` | No need to import a separate `Select` class; accepts `value`, label (`label="Option"`), or `index`. |
| **Checkbox / Radio** | `if not element.is_selected(): element.click()` | `locator.check()` / `locator.uncheck()` | `.check()` is **idempotent**: if already checked, it performs no action. |
| **Hover** | `ActionChains(driver).move_to_element(el).perform()` | `locator.hover()` | No need to instantiate or chain action classes. |
| **Wait for Visibility** | `WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))` | `locator.wait_for(state="visible")` | Rarely needed manually because actions auto-wait automatically. |
| **Assertions (Validate)** | `assert "Hello" in element.text` | `expect(locator).to_have_text("Hello")` | `expect()` retries automatically with a configurable timeout until the assertion passes. |

---

## 6. Strategic Interview Q&A

### 1. Why use Pytest-BDD over Behave?
- **Native Parallelism**: `pytest-xdist` allows running hundreds of Gherkin scenarios concurrently across CPU cores without flaky hacks.
- **Dependency Injection**: Pytest fixtures eliminate the shared, mutable `context` anti-pattern, providing scoped setup/teardown and rock-solid IDE navigation.
- **Ecosystem**: Direct access to Pytest plugins (`pytest-rerunfailures` for flaky tests, `allure-pytest` for reporting, `pytest-html`).

### 2. Why keep assertions out of `BasePage`? (Clean POM)
- **Single Responsibility Principle (SRP)**: Page Objects model UI state and actions; step definitions own the verification and business expectations.
- **Reusability**: Decoupling assertions allows reusing the exact same Page Object methods across positive and negative testing flows.
