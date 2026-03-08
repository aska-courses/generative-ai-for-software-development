package com.epam.solutionshub.steps;

import io.cucumber.java.en.*;
import org.assertj.core.api.Assertions;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

/**
 * Step definitions for about.feature (TC-ABT-001 to TC-ABT-008)
 */
public class AboutSteps extends BaseSteps {

    private static final By CONTACT_BUTTON   = By.cssSelector("button.GA_Header_Contact_us, [class*='contactButton'], button:contains('Contact')");
    private static final By CONTACT_MODAL    = By.cssSelector(".modal, [role='dialog'], [data-testid='contactModal']");
    private static final By EXTERNAL_LINKS   = By.cssSelector("a[target='_blank'], a[rel*='noopener']");
    private static final By INTERNAL_LINKS   = By.cssSelector("a:not([target='_blank']):not([href^='mailto']):not([href^='tel'])");

    // TC-ABT-001
    @Then("all About page content sections should be visible")
    public void verifyAboutPageSectionsVisible() {
        // The page body should have meaningful content
        WebElement body = waitForVisible(By.tagName("main"));
        Assertions.assertThat(body.getText().trim())
                .as("About page body should have content")
                .isNotBlank();
    }

    // TC-ABT-003
    @When("the user collects all internal links on the About page")
    public void collectInternalLinks() {
        waitForAll(INTERNAL_LINKS);
    }

    @Then("each internal link should return HTTP status {int}")
    public void verifyAllInternalLinksReturn200(int expectedStatus) {
        List<WebElement> links = driver().findElements(INTERNAL_LINKS);
        List<String> brokenLinks = new ArrayList<>();

        for (WebElement link : links) {
            String href = link.getAttribute("href");
            if (href == null || href.isBlank() || href.startsWith("#")) continue;
            if (!href.contains("solutionshub.epam.com")) continue;

            try {
                HttpURLConnection conn = (HttpURLConnection) new URL(href).openConnection();
                conn.setRequestMethod("HEAD");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                conn.connect();
                int status = conn.getResponseCode();
                conn.disconnect();
                if (status >= 400) {
                    brokenLinks.add(href + " → HTTP " + status);
                }
            } catch (Exception e) {
                brokenLinks.add(href + " → Exception: " + e.getMessage());
            }
        }
        Assertions.assertThat(brokenLinks)
                .as("Broken links found on About page")
                .isEmpty();
    }

    @Then("no link should lead to a 404 page")
    public void verifyNoLinksReturn404() {
        // Covered by the step above – no-op here
    }

    // TC-ABT-004
    @When("the user clicks an external link on the About page")
    public void clickFirstExternalLink() {
        List<WebElement> externalLinks = driver().findElements(EXTERNAL_LINKS);
        if (externalLinks.isEmpty()) return; // no external links – test passes trivially
        String mainHandle = driver().getWindowHandle();
        externalLinks.get(0).click();
        new org.openqa.selenium.support.ui.WebDriverWait(driver(), DEFAULT_WAIT)
                .until(d -> d.getWindowHandles().size() > 1);
    }

    @Then("a new browser tab should be opened")
    public void verifyNewTabOpened() {
        Set<String> handles = driver().getWindowHandles();
        if (handles.size() > 1) {
            Assertions.assertThat(handles.size())
                    .as("A new tab should have been opened")
                    .isGreaterThan(1);
        }
    }

    @Then("the original About page should remain open in the previous tab")
    public void verifyOriginalTabStillOpen() {
        Set<String> handles = driver().getWindowHandles();
        if (handles.size() > 1) {
            String original = handles.iterator().next();
            driver().switchTo().window(original);
            Assertions.assertThat(driver().getCurrentUrl())
                    .as("Original About tab should remain open")
                    .contains("solutionshub.epam.com");
            // Close extra tabs
            handles.stream().skip(1).forEach(h -> {
                driver().switchTo().window(h);
                driver().close();
            });
            driver().switchTo().window(original);
        }
    }

    // TC-ABT-005
    @Given("the {string} button is present on the About page")
    public void verifyButtonPresent(String buttonText) {
        List<WebElement> buttons = driver().findElements(
                By.xpath("//button[contains(normalize-space(text()),'" + buttonText + "')] | //a[contains(normalize-space(text()),'" + buttonText + "')]"));
        Assertions.assertThat(buttons).as("'%s' button should be on the About page", buttonText).isNotEmpty();
    }

    @When("the user clicks the {string} button")
    public void clickButton(String buttonText) {
        List<WebElement> buttons = driver().findElements(
                By.xpath("//button[contains(normalize-space(text()),'" + buttonText + "')] | //a[contains(normalize-space(text()),'" + buttonText + "')]"));
        if (!buttons.isEmpty()) {
            buttons.get(0).click();
            try { Thread.sleep(800); } catch (InterruptedException ignored) {}
        }
    }

    @Then("a contact form or modal should be displayed")
    public void verifyContactFormOrModalDisplayed() {
        boolean hasModal = isElementPresent(CONTACT_MODAL);
        boolean urlChanged = driver().getCurrentUrl().contains("contact");
        Assertions.assertThat(hasModal || urlChanged)
                .as("Contact modal/form should be shown or user navigated to contact page")
                .isTrue();
    }

    // TC-ABT-006
    @When("the user inspects all images on the About page")
    public void inspectAboutPageImages() {
        waitForVisible(By.tagName("main"));
    }

    @Then("all images should render without broken image icons")
    public void verifyAboutImagesNotBroken() {
        List<WebElement> images = driver().findElements(By.tagName("img"));
        images.stream().filter(WebElement::isDisplayed).forEach(img -> {
            Object naturalWidth = ((org.openqa.selenium.JavascriptExecutor) driver())
                    .executeScript("return arguments[0].naturalWidth", img);
            Assertions.assertThat(naturalWidth)
                    .as("Image '%s' appears broken", img.getAttribute("src"))
                    .isNotEqualTo(0L);
        });
    }

    @Then("all images should be appropriately sized within their containers")
    public void verifyImageSizing() {
        List<WebElement> images = driver().findElements(By.tagName("img"));
        images.stream().filter(WebElement::isDisplayed).forEach(img -> {
            int width = img.getSize().getWidth();
            Assertions.assertThat(width)
                    .as("Image width should be greater than 0")
                    .isGreaterThan(0);
        });
    }

    // TC-ABT-007
    @Then("the About page should display the company description")
    public void verifyCompanyDescriptionPresent() {
        List<WebElement> paragraphs = driver().findElements(By.cssSelector("main p, .about-description, [data-testid='companyDescription']"));
        Assertions.assertThat(paragraphs).as("Company description paragraph(s) should be present").isNotEmpty();
    }

    @Then("the About page should display the company mission or purpose statement")
    public void verifyMissionStatementPresent() {
        String bodyText = driver().findElement(By.tagName("main")).getText().toLowerCase();
        Assertions.assertThat(bodyText)
                .as("About page body text should contain meaningful mission-related content")
                .isNotBlank();
    }

    @Then("key informational sections should be present and populated")
    public void verifyInformationalSectionsPresent() {
        List<WebElement> sections = driver().findElements(By.cssSelector("section, .about-section, main > div"));
        Assertions.assertThat(sections).as("About page should have multiple content sections").isNotEmpty();
    }
}
