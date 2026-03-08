# SolutionsHub BDD Test Suite

Cucumber + JUnit5 + Selenium test suite for https://solutionshub.epam.com/

## Tech Stack

| Tool | Version |
|------|---------|
| Java | 11 |
| Gradle | 8.5 |
| JUnit 5 | 5.10.1 |
| Cucumber | 7.15.0 |
| Selenium | 4.16.1 |
| WebDriverManager | 5.6.3 |
| AssertJ | 3.24.2 |

---

## Project Structure

```
solutionshub-bdd/
├── build.gradle
├── settings.gradle
└── src/test/
    ├── java/com/epam/solutionshub/
    │   ├── hooks/
    │   │   └── Hooks.java                  # WebDriver setup/teardown + screenshots
    │   ├── runners/
    │   │   └── AllFeaturesRunner.java       # JUnit5 Suite runner
    │   └── steps/
    │       ├── BaseSteps.java               # Shared Selenium utilities
    │       ├── CommonSteps.java             # Reused steps (navigation, HTTP, nav bar)
    │       ├── SolutionsSteps.java          # Steps for Solutions tab
    │       ├── AssetsSteps.java             # Steps for Assets tab
    │       ├── GuidesSteps.java             # Steps for Guides tab
    │       ├── BlogSteps.java               # Steps for Blog tab
    │       └── AboutSteps.java             # Steps for About tab
    └── resources/
        ├── features/
        │   ├── solutions/solutions.feature  # TC-SOL-001 to TC-SOL-010
        │   ├── assets/assets.feature        # TC-ASS-001 to TC-ASS-009
        │   ├── guides/guides.feature        # TC-GUI-001 to TC-GUI-006
        │   ├── blog/blog.feature            # TC-BLG-001 to TC-BLG-008
        │   └── about/about.feature          # TC-ABT-001 to TC-ABT-008
        ├── cucumber.properties
        └── junit-platform.properties
```

---

## Running Tests

### Prerequisites
- Java 11+
- Chrome browser installed (ChromeDriver managed automatically)

### Commands

```bash
# Run all tests
./gradlew test

# Run only smoke tests (fast sanity check)
./gradlew test -Dcucumber.filter.tags="@smoke"

# Run regression tests
./gradlew test -Dcucumber.filter.tags="@regression"

# Run responsive/mobile tests
./gradlew test -Dcucumber.filter.tags="@responsive"

# Run a single tab
./gradlew test -Dcucumber.filter.tags="@solutions"
./gradlew test -Dcucumber.filter.tags="@assets"
./gradlew test -Dcucumber.filter.tags="@blog"

# Exclude work-in-progress scenarios
./gradlew test -Dcucumber.filter.tags="not @wip"

# Combine tags
./gradlew test -Dcucumber.filter.tags="@smoke and @solutions"
```

---

## Test Coverage

| Tab       | Tag          | Scenarios | TC IDs               |
|-----------|--------------|-----------|----------------------|
| Solutions | @solutions   | 10        | TC-SOL-001–010       |
| Assets    | @assets      | 9         | TC-ASS-001–009       |
| Guides    | @guides      | 6         | TC-GUI-001–006       |
| Blog      | @blog        | 8         | TC-BLG-001–008       |
| About     | @about       | 8         | TC-ABT-001–008       |
| **Total** |              | **41**    |                      |

### Tag Matrix

| Tag          | Purpose                         |
|--------------|---------------------------------|
| `@smoke`     | Critical path – run on every CI |
| `@regression`| Full regression suite           |
| `@responsive`| Viewport/mobile scenarios       |
| `@wip`       | Work in progress – excluded     |

---

## Reports

After test execution, HTML and JSON reports are generated:

```
build/reports/cucumber/report.html   ← Human-readable
build/reports/cucumber/report.json   ← For CI/CD integration
```

---

## Configuration

Edit `src/test/resources/junit-platform.properties` to change:
- `cucumber.filter.tags` – default tag filter
- `cucumber.plugin` – report formats and paths
- `cucumber.glue` – step definition packages
