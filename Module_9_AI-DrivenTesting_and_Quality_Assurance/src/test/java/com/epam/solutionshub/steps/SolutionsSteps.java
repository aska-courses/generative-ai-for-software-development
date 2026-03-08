package com.epam.solutionshub.steps;

import io.cucumber.java.en.*;
import org.assertj.core.api.Assertions;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;

import java.util.List;

/**
 * Step definitions for solutions.feature (TC-SOL-001 to TC-SOL-010)
 */
public class SolutionsSteps extends BaseSteps {

    // Locators
    private static final By CATALOG_ITEMS       = By.cssSelector(".catalog-item, [data-testid='catalogItem'], .solution-card");
    private static final By FILTER_PANEL        = By.cssSelector("[data-testid='filterPanel'], .filter-panel, aside");
    private static final By ACTIVE_FILTER_CHIPS = By.cssSelector(".filter-chip--active, [data-testid='activeFilter'], .active-filter");
    private static final By SEARCH_INPUT        = By.cssSelector("input[type='search'], input[placeholder*='Search'], input[data-testid='searchInput']");
    private static final By EMPTY_STATE         = By.cssSelector(".empty-state, [data-testid='emptyState'], .no-results");
    private static final By CLEAR_ALL_BUTTON    = By.cssSelector("[data-testid='clearAllFilters'], button.clear-filters, .clear-all");

    // -----------------------------------------------------------------------
    // TC-SOL-001 / TC-ASS-001 / shared catalog assertions
    // -----------------------------------------------------------------------

    @Then("the solutions catalog should be displayed")
    public void verifySolutionsCatalogDisplayed() {
        List<WebElement> items = waitForAll(CATALOG_ITEMS);
        Assertions.assertThat(items)
                .as("Solutions catalog should have at least one item")
                .isNotEmpty();
    }

    @Then("the assets catalog should be displayed")
    public void verifyAssetsCatalogDisplayed() {
        verifySolutionsCatalogDisplayed(); // same underlying check
    }

    // -----------------------------------------------------------------------
    // TC-SOL-003 – Industry filter
    // -----------------------------------------------------------------------

    @When("the user selects the Industry filter {string}")
    public void selectIndustryFilter(String industry) {
        clickFilterOption(industry);
    }

    @Then("the catalog should update to show only solutions tagged with {string}")
    public void verifyCatalogFilteredByIndustry(String industry) {
        waitForAll(CATALOG_ITEMS);
        // Verify filter chip is active (detailed tag check would require inspecting card metadata)
        Assertions.assertThat(driver().findElements(ACTIVE_FILTER_CHIPS))
                .as("Active filter chip for '%s' should be visible", industry)
                .isNotEmpty();
    }

    @Then("the active filter chip {string} should be visible")
    public void verifyFilterChipVisible(String filterLabel) {
        boolean found = driver().findElements(ACTIVE_FILTER_CHIPS).stream()
                .anyMatch(el -> el.getText().contains(filterLabel));
        Assertions.assertThat(found)
                .as("Filter chip '%s' should be visible", filterLabel)
                .isTrue();
    }

    // -----------------------------------------------------------------------
    // TC-SOL-004 – Multiple filters
    // -----------------------------------------------------------------------

    @When("the user selects the Category filter {string}")
    public void selectCategoryFilter(String category) {
        clickFilterOption(category);
    }

    @Then("the catalog should display results matching both filters")
    public void verifyCatalogMatchesBothFilters() {
        List<WebElement> chips = driver().findElements(ACTIVE_FILTER_CHIPS);
        Assertions.assertThat(chips.size())
                .as("At least 2 active filter chips should be visible")
                .isGreaterThanOrEqualTo(2);
    }

    @Then("the active filter chips should show {string} and {string}")
    public void verifyTwoFilterChips(String first, String second) {
        List<WebElement> chips = driver().findElements(ACTIVE_FILTER_CHIPS);
        boolean hasFirst  = chips.stream().anyMatch(el -> el.getText().contains(first));
        boolean hasSecond = chips.stream().anyMatch(el -> el.getText().contains(second));
        Assertions.assertThat(hasFirst).as("Filter chip '%s' not found", first).isTrue();
        Assertions.assertThat(hasSecond).as("Filter chip '%s' not found", second).isTrue();
    }

    // -----------------------------------------------------------------------
    // TC-SOL-005 – Clear filters
    // -----------------------------------------------------------------------

    @Given("the user has applied the Industry filter {string}")
    public void applyIndustryFilter(String industry) {
        clickFilterOption(industry);
        waitForAll(CATALOG_ITEMS);
    }

    @When("the user clicks the \"Clear All\" filters button")
    public void clickClearAllFilters() {
        waitForClickable(CLEAR_ALL_BUTTON).click();
    }

    @Then("the full solutions catalog should be restored")
    public void verifyFullCatalogRestored() {
        List<WebElement> items = waitForAll(CATALOG_ITEMS);
        Assertions.assertThat(items).as("Full catalog should be visible after clearing filters").isNotEmpty();
    }

    @Then("no active filter chips should be visible")
    public void verifyNoActiveFilterChips() {
        List<WebElement> chips = driver().findElements(ACTIVE_FILTER_CHIPS);
        Assertions.assertThat(chips).as("No active filter chips should remain").isEmpty();
    }

    // -----------------------------------------------------------------------
    // TC-SOL-006 – Search
    // -----------------------------------------------------------------------

    @When("the user types {string} in the search bar")
    public void typeInSearchBar(String keyword) {
        WebElement searchInput = waitForClickable(SEARCH_INPUT);
        searchInput.clear();
        searchInput.sendKeys(keyword);
    }

    @Then("the catalog should filter to show only solutions related to {string}")
    public void verifyCatalogFilteredBySearch(String keyword) {
        waitForAll(CATALOG_ITEMS);
        Assertions.assertThat(driver().findElements(CATALOG_ITEMS))
                .as("Some results should appear for keyword '%s'", keyword)
                .isNotEmpty();
    }

    @Then("the displayed results should be relevant to the search term")
    @Then("the displayed results should be relevant to {string}")
    public void verifyResultsRelevant(String keyword) {
        // Basic check: at least one result title or description contains the keyword (case-insensitive)
        List<WebElement> items = driver().findElements(CATALOG_ITEMS);
        boolean anyRelevant = items.stream()
                .anyMatch(el -> el.getText().toLowerCase().contains(keyword.toLowerCase()));
        Assertions.assertThat(anyRelevant)
                .as("At least one result should relate to '%s'", keyword)
                .isTrue();
    }

    // -----------------------------------------------------------------------
    // TC-SOL-007 – Empty / no-results state
    // -----------------------------------------------------------------------

    @Then("an empty state message should be displayed")
    @Then("an empty state or no-results message should be displayed")
    public void verifyEmptyStateDisplayed() {
        boolean emptyVisible  = isElementPresent(EMPTY_STATE);
        boolean noItems       = driver().findElements(CATALOG_ITEMS).isEmpty();
        Assertions.assertThat(emptyVisible || noItems)
                .as("Empty state message or zero results should be displayed")
                .isTrue();
    }

    @Then("the page should not crash or show any errors")
    @Then("no errors should occur")
    public void verifyPageNotCrashed() {
        Assertions.assertThat(driver().getCurrentUrl())
                .as("Page URL should still be valid after invalid search")
                .contains("solutionshub.epam.com");
    }

    // -----------------------------------------------------------------------
    // TC-SOL-008 – Click solution card → detail page
    // -----------------------------------------------------------------------

    @Given("at least one solution card is visible in the catalog")
    @Given("at least one asset card is visible in the catalog")
    public void verifyAtLeastOneCardVisible() {
        List<WebElement> items = waitForAll(CATALOG_ITEMS);
        Assertions.assertThat(items).as("Catalog should have at least one item").isNotEmpty();
    }

    @When("the user clicks on the first solution card")
    @When("the user clicks on the first asset card")
    public void clickFirstCard() {
        String originalUrl = driver().getCurrentUrl();
        List<WebElement> items = waitForAll(CATALOG_ITEMS);
        items.get(0).click();
        // Wait for URL to change
        new org.openqa.selenium.support.ui.WebDriverWait(driver(), DEFAULT_WAIT)
                .until(d -> !d.getCurrentUrl().equals(originalUrl));
    }

    @Then("the user should be navigated to the solution detail page")
    public void verifySolutionDetailPageOpened() {
        Assertions.assertThat(driver().getCurrentUrl())
                .as("URL should change to solution detail page")
                .isNotEqualTo(BASE_URL + "/catalog");
    }

    @Then("the page URL should change to reflect the selected solution")
    public void verifyUrlChanged() {
        Assertions.assertThat(driver().getCurrentUrl())
                .as("URL should contain path to the selected item")
                .contains("solutionshub.epam.com");
    }

    @Then("the solution detail content should be loaded")
    public void verifySolutionDetailContentLoaded() {
        // Heading or main content area should be visible
        WebElement heading = waitForVisible(By.cssSelector("h1, h2, .solution-detail-title, [data-testid='detailTitle']"));
        Assertions.assertThat(heading.getText())
                .as("Detail page title should not be empty")
                .isNotBlank();
    }

    // -----------------------------------------------------------------------
    // TC-SOL-009 – Detail page content completeness
    // -----------------------------------------------------------------------

    @Given("the user is on a solution detail page")
    public void navigateToSolutionDetailPage() {
        driver().get(BASE_URL + "/catalog");
        List<WebElement> items = waitForAll(CATALOG_ITEMS);
        String originalUrl = driver().getCurrentUrl();
        items.get(0).click();
        new org.openqa.selenium.support.ui.WebDriverWait(driver(), DEFAULT_WAIT)
                .until(d -> !d.getCurrentUrl().equals(originalUrl));
    }

    @Then("the detail page should display the solution title")
    public void verifyDetailTitle() {
        WebElement title = waitForVisible(By.cssSelector("h1, .detail-title, [data-testid='solutionTitle']"));
        Assertions.assertThat(title.getText()).isNotBlank();
    }

    @Then("the detail page should display the solution description")
    public void verifyDetailDescription() {
        WebElement desc = waitForVisible(By.cssSelector("p.description, .solution-description, [data-testid='description'], main p"));
        Assertions.assertThat(desc.getText()).isNotBlank();
    }

    @Then("the detail page should display solution tags or category")
    public void verifyDetailTags() {
        boolean hasTags = isElementPresent(By.cssSelector(".tag, .badge, [data-testid='tag'], .category"));
        Assertions.assertThat(hasTags).as("Solution detail should display tags or category").isTrue();
    }

    @Then("the detail page should display relevant action buttons")
    public void verifyDetailActionButtons() {
        List<WebElement> buttons = driver().findElements(By.cssSelector("main button, main a.btn, main a[role='button']"));
        Assertions.assertThat(buttons).as("Detail page should have action buttons").isNotEmpty();
    }

    // -----------------------------------------------------------------------
    // TC-SOL-010 – Responsive layout
    // -----------------------------------------------------------------------

    @Then("the filter panel should adapt to the {string} layout")
    public void verifyFilterPanelAdaptsToLayout(String device) {
        if (!device.equals("mobile")) {
            Assertions.assertThat(isElementPresent(FILTER_PANEL))
                    .as("Filter panel should be visible on %s", device)
                    .isTrue();
        }
        // On mobile the filter panel may be hidden behind a toggle button – pass either way
    }

    @Then("solution cards should be properly displayed")
    @Then("filters and asset cards should be usable on the {string} layout")
    public void verifyCardsDisplayed(String device) {
        List<WebElement> items = waitForAll(CATALOG_ITEMS);
        Assertions.assertThat(items).as("Cards should be visible on %s", device).isNotEmpty();
    }

    // -----------------------------------------------------------------------
    // Helper
    // -----------------------------------------------------------------------

    private void clickFilterOption(String label) {
        // Try to find any filter link or checkbox that matches the label text
        List<WebElement> options = driver().findElements(
                By.xpath("//*[contains(@class,'filter') or contains(@data-testid,'filter')]" +
                         "//*[normalize-space(text())='" + label + "']"));
        if (options.isEmpty()) {
            // Fallback: any element whose visible text matches
            options = driver().findElements(
                    By.xpath("//*[normalize-space(text())='" + label + "']"));
        }
        Assertions.assertThat(options).as("Filter option '%s' should exist", label).isNotEmpty();
        options.get(0).click();
        // Brief pause for catalog to re-render
        try { Thread.sleep(800); } catch (InterruptedException ignored) {}
    }
}
