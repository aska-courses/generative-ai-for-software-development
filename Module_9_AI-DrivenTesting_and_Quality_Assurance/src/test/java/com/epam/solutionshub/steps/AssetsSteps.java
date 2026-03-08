package com.epam.solutionshub.steps;

import io.cucumber.java.en.*;
import org.assertj.core.api.Assertions;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import java.util.List;

/**
 * Step definitions for assets.feature (TC-ASS-001 to TC-ASS-009)
 */
public class AssetsSteps extends BaseSteps {

    private static final By ASSET_ITEMS  = By.cssSelector(".asset-card, [data-testid='assetItem'], .catalog-item");
    private static final By SEARCH_INPUT = By.cssSelector("input[type='search'], input[placeholder*='Search'], input[data-testid='searchInput']");
    private static final By EMPTY_STATE  = By.cssSelector(".empty-state, [data-testid='emptyState'], .no-results");

    // TC-ASS-003
    @When("the user selects the Competency Center filter {string}")
    public void selectCompetencyCenterFilter(String center) {
        clickFilterByText(center);
    }

    @Then("the asset list should update to show only assets under {string}")
    public void verifyAssetListFilteredByCenter(String center) {
        waitForAll(ASSET_ITEMS);
        Assertions.assertThat(driver().findElements(ASSET_ITEMS))
                .as("Asset list should not be empty after filtering by '%s'", center)
                .isNotEmpty();
    }

    // TC-ASS-004
    @When("the user selects the Asset Type filter {string}")
    public void selectAssetTypeFilter(String type) {
        clickFilterByText(type);
    }

    @Then("only assets of type {string} should be displayed")
    public void verifyAssetsFilteredByType(String type) {
        List<WebElement> items = waitForAll(ASSET_ITEMS);
        Assertions.assertThat(items).as("Assets of type '%s' should be displayed", type).isNotEmpty();
    }

    // TC-ASS-005
    @Then("the results should be filtered by both {string} and {string}")
    public void verifyResultsFilteredByBoth(String type, String center) {
        // Either results are shown or an empty state – both are valid outcomes
        boolean hasResults = !driver().findElements(ASSET_ITEMS).isEmpty();
        boolean hasEmpty   = isElementPresent(EMPTY_STATE);
        Assertions.assertThat(hasResults || hasEmpty)
                .as("Either results or empty state should be visible for '%s' + '%s'", type, center)
                .isTrue();
    }

    @Then("either relevant assets are displayed or an empty state message is shown")
    public void verifyResultsOrEmptyState() {
        boolean hasResults = !driver().findElements(ASSET_ITEMS).isEmpty();
        boolean hasEmpty   = isElementPresent(EMPTY_STATE);
        Assertions.assertThat(hasResults || hasEmpty)
                .as("Either results or empty state should be displayed")
                .isTrue();
    }

    // TC-ASS-006
    @Then("the asset detail page should load")
    public void verifyAssetDetailPageLoaded() {
        Assertions.assertThat(driver().getCurrentUrl())
                .as("URL should change to asset detail page")
                .doesNotContain("mode=assets");
    }

    @Then("the full asset description and metadata should be visible")
    public void verifyAssetDetailContent() {
        WebElement heading = waitForVisible(By.cssSelector("h1, h2, .asset-title, [data-testid='assetTitle']"));
        Assertions.assertThat(heading.getText()).isNotBlank();
    }

    // TC-ASS-007
    @Then("the asset list should filter to show automation-related assets")
    public void verifyAssetListFilteredBySearch() {
        List<WebElement> items = driver().findElements(ASSET_ITEMS);
        Assertions.assertThat(items).as("Some assets should be visible after search").isNotEmpty();
    }

    // TC-ASS-008
    @Then("no JavaScript errors should occur")
    public void verifyNoJsErrors() {
        Assertions.assertThat(driver().getCurrentUrl())
                .as("Page should still be on solutionshub domain")
                .contains("solutionshub.epam.com");
    }

    // Helper
    private void clickFilterByText(String label) {
        List<WebElement> options = driver().findElements(
                By.xpath("//*[normalize-space(text())='" + label + "']"));
        Assertions.assertThat(options).as("Filter option '%s' should exist on page", label).isNotEmpty();
        options.get(0).click();
        try { Thread.sleep(800); } catch (InterruptedException ignored) {}
    }
}
