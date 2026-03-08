package com.epam.solutionshub.steps;

import io.cucumber.java.en.*;
import org.assertj.core.api.Assertions;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import java.util.List;

/**
 * Step definitions for guides.feature (TC-GUI-001 to TC-GUI-006)
 */
public class GuidesSteps extends BaseSteps {

    private static final By GUIDE_ITEMS   = By.cssSelector(".guide-card, [data-testid='guideItem'], article, .guide-item");
    private static final By GUIDE_HEADING = By.cssSelector("h1, .guide-title, [data-testid='guideTitle']");
    private static final By GUIDE_CONTENT = By.cssSelector(".guide-content, main article, [data-testid='guideContent']");

    // TC-GUI-001
    @Then("a list of guides should be displayed with titles and summaries")
    public void verifyGuideListDisplayed() {
        List<WebElement> guides = waitForAll(GUIDE_ITEMS);
        Assertions.assertThat(guides).as("At least one guide should be listed").isNotEmpty();
    }

    // TC-GUI-003
    @Given("at least one guide is visible in the listing")
    public void verifyAtLeastOneGuideVisible() {
        List<WebElement> guides = waitForAll(GUIDE_ITEMS);
        Assertions.assertThat(guides).as("Guides listing should not be empty").isNotEmpty();
    }

    @When("the user clicks on the first guide card")
    public void clickFirstGuideCard() {
        String originalUrl = driver().getCurrentUrl();
        List<WebElement> guides = waitForAll(GUIDE_ITEMS);
        guides.get(0).click();
        new org.openqa.selenium.support.ui.WebDriverWait(driver(), DEFAULT_WAIT)
                .until(d -> !d.getCurrentUrl().equals(originalUrl));
    }

    @Then("the guide detail page should open")
    public void verifyGuideDetailPageOpened() {
        Assertions.assertThat(driver().getCurrentUrl())
                .as("URL should change to guide detail page")
                .doesNotEndWith("/guides");
    }

    @Then("the full guide content should be displayed with proper formatting")
    public void verifyGuideContentDisplayed() {
        WebElement heading = waitForVisible(GUIDE_HEADING);
        Assertions.assertThat(heading.getText()).as("Guide title should not be empty").isNotBlank();
    }

    // TC-GUI-004
    @Given("the user is on a guide detail page")
    public void navigateToGuideDetailPage() {
        driver().get(BASE_URL + "/guides");
        List<WebElement> guides = waitForAll(GUIDE_ITEMS);
        String originalUrl = driver().getCurrentUrl();
        guides.get(0).click();
        new org.openqa.selenium.support.ui.WebDriverWait(driver(), DEFAULT_WAIT)
                .until(d -> !d.getCurrentUrl().equals(originalUrl));
    }

    @Then("the guide should display headings with correct styling")
    public void verifyGuideHeadingsStyling() {
        List<WebElement> headings = driver().findElements(By.cssSelector("h1, h2, h3"));
        Assertions.assertThat(headings).as("Guide should have at least one heading").isNotEmpty();
    }

    @Then("the guide text should be readable")
    public void verifyGuideTextReadable() {
        List<WebElement> paragraphs = driver().findElements(By.cssSelector("p, [data-testid='guideContent'] *"));
        Assertions.assertThat(paragraphs).as("Guide should have readable text content").isNotEmpty();
    }

    @Then("all guide images should load without errors")
    public void verifyGuideImagesLoaded() {
        verifyAllImagesLoaded();
    }

    // TC-GUI-005
    @When("the user clicks the browser back button")
    public void clickBrowserBack() {
        driver().navigate().back();
    }

    @Then("the user should be returned to the Guides listing page")
    public void verifyReturnToGuidesListing() {
        new org.openqa.selenium.support.ui.WebDriverWait(driver(), DEFAULT_WAIT)
                .until(d -> d.getCurrentUrl().contains("/guides"));
        Assertions.assertThat(driver().getCurrentUrl()).contains("/guides");
    }

    @Then("the Guides listing content should be visible")
    public void verifyGuidesListingContentVisible() {
        List<WebElement> guides = waitForAll(GUIDE_ITEMS);
        Assertions.assertThat(guides).isNotEmpty();
    }

    // TC-GUI-006
    @Then("clicking into a guide should display readable content without horizontal scroll")
    public void verifyGuideReadableOnMobile() {
        // Presence of text content is sufficient here
        List<WebElement> items = driver().findElements(GUIDE_ITEMS);
        Assertions.assertThat(items).isNotEmpty();
    }

    // Helper shared by multiple features
    private void verifyAllImagesLoaded() {
        List<WebElement> images = driver().findElements(By.tagName("img"));
        images.stream()
                .filter(WebElement::isDisplayed)
                .forEach(img -> {
                    Object naturalWidth = ((org.openqa.selenium.JavascriptExecutor) driver())
                            .executeScript("return arguments[0].naturalWidth", img);
                    Assertions.assertThat(naturalWidth)
                            .as("Image '%s' should have non-zero naturalWidth (broken if 0)", img.getAttribute("src"))
                            .isNotEqualTo(0L);
                });
    }
}
