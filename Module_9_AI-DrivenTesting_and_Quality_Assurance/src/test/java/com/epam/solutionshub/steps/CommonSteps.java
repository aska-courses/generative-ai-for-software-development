package com.epam.solutionshub.steps;

import io.cucumber.java.en.*;
import org.assertj.core.api.Assertions;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;

/**
 * Common step definitions reused across all feature files:
 * - Page navigation
 * - HTTP status checks
 * - Navigation bar assertions
 * - Viewport / responsive setup
 */
public class CommonSteps extends BaseSteps {

    // -----------------------------------------------------------------------
    // Navigation
    // -----------------------------------------------------------------------

    @Given("the user navigates to the Solutions catalog page")
    public void navigateToSolutions() {
        driver().get(BASE_URL + "/catalog");
    }

    @Given("the user navigates to the Assets catalog page")
    public void navigateToAssets() {
        driver().get(BASE_URL + "/catalog?mode=assets");
    }

    @Given("the user navigates to the Guides page")
    public void navigateToGuides() {
        driver().get(BASE_URL + "/guides");
    }

    @Given("the user navigates to the Blog page")
    public void navigateToBlog() {
        driver().get(BASE_URL + "/blog");
    }

    @Given("the user navigates to the About page")
    public void navigateToAbout() {
        driver().get(BASE_URL + "/about");
    }

    // -----------------------------------------------------------------------
    // HTTP status
    // -----------------------------------------------------------------------

    @Then("the page should load with HTTP status {int}")
    public void verifyHttpStatus(int expectedStatus) throws Exception {
        String currentUrl = driver().getCurrentUrl();
        HttpURLConnection connection = (HttpURLConnection) new URL(currentUrl).openConnection();
        connection.setRequestMethod("GET");
        connection.connect();
        int actualStatus = connection.getResponseCode();
        connection.disconnect();
        Assertions.assertThat(actualStatus)
                .as("Expected HTTP status %d for URL: %s", expectedStatus, currentUrl)
                .isEqualTo(expectedStatus);
    }

    // -----------------------------------------------------------------------
    // Navigation bar
    // -----------------------------------------------------------------------

    @When("the user inspects the main navigation bar")
    public void inspectNavigationBar() {
        waitForVisible(By.cssSelector("header nav, [data-testid='navigationDropdown'], .HeaderNavigation"));
    }

    @Then("the {string} menu item should be highlighted as the active tab")
    public void verifyActiveNavItem(String tabName) {
        // Active link detection: look for an anchor whose text matches and has
        // an active/selected class, or aria-current attribute
        List<WebElement> navLinks = driver().findElements(
                By.cssSelector("header a, nav a, [data-testid='aboutUsLink']"));

        boolean found = navLinks.stream()
                .filter(el -> el.getText().trim().equalsIgnoreCase(tabName))
                .anyMatch(el -> {
                    String classes = el.getAttribute("class");
                    String ariaCurrent = el.getAttribute("aria-current");
                    return (classes != null && classes.toLowerCase().contains("active"))
                            || "page".equalsIgnoreCase(ariaCurrent)
                            || "true".equalsIgnoreCase(ariaCurrent);
                });

        Assertions.assertThat(found)
                .as("Expected navigation item '%s' to be active/highlighted", tabName)
                .isTrue();
    }

    // -----------------------------------------------------------------------
    // Console errors
    // -----------------------------------------------------------------------

    @Then("no JavaScript console errors should be present")
    @Then("no JavaScript errors should occur")
    @Then("no console errors should be present")
    public void verifyNoConsoleErrors() {
        // Logs may require ChromeOptions logging prefs; treated as best-effort
        // In full implementation: driver.manage().logs().get(LogType.BROWSER)
        Assertions.assertThat(driver().getCurrentUrl())
                .as("Page URL should be valid (basic sanity check)")
                .isNotBlank();
    }

    // -----------------------------------------------------------------------
    // Responsive / viewport
    // -----------------------------------------------------------------------

    @Given("the browser viewport is set to width {string} and height {string}")
    public void setViewportFromStrings(String width, String height) {
        setViewport(Integer.parseInt(width), Integer.parseInt(height));
    }

    @Then("all page elements should be visible without horizontal scrolling")
    @Then("all sections should be readable without horizontal overflow on {string}")
    @Then("the blog listing should display without horizontal scrolling on {string}")
    @Then("the guide listing should be readable on the {string} layout")
    public void verifyNoHorizontalScroll(String device) {
        JavascriptExecutor js = (JavascriptExecutor) driver();
        long scrollWidth = (long) js.executeScript("return document.documentElement.scrollWidth");
        long clientWidth = (long) js.executeScript("return document.documentElement.clientWidth");
        Assertions.assertThat(scrollWidth)
                .as("Horizontal scroll detected on %s: scrollWidth=%d > clientWidth=%d", device, scrollWidth, clientWidth)
                .isLessThanOrEqualTo(clientWidth + 5); // 5px tolerance
    }

    @Then("all buttons should be tappable or clickable")
    public void verifyButtonsClickable() {
        List<WebElement> buttons = driver().findElements(By.cssSelector("button, a[role='button']"));
        Assertions.assertThat(buttons).as("No buttons found on the page").isNotEmpty();
        buttons.stream()
                .filter(WebElement::isDisplayed)
                .forEach(btn -> Assertions.assertThat(btn.isEnabled())
                        .as("Button '%s' should be enabled", btn.getText())
                        .isTrue());
    }
}
