package com.epam.solutionshub.steps;

import com.epam.solutionshub.hooks.Hooks;
import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

/**
 * Shared Selenium utilities available to all step definition classes.
 * Cucumber instantiates step classes via PicoContainer DI, so all step
 * classes share the same driver instance through Hooks.getDriver().
 */
public class BaseSteps {

    protected static final String BASE_URL = "https://solutionshub.epam.com";
    protected static final Duration DEFAULT_WAIT = Duration.ofSeconds(15);

    protected WebDriver driver() {
        return Hooks.getDriver();
    }

    protected WebDriverWait wait() {
        return new WebDriverWait(driver(), DEFAULT_WAIT);
    }

    protected WebElement waitForVisible(By locator) {
        return wait().until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    protected WebElement waitForClickable(By locator) {
        return wait().until(ExpectedConditions.elementToBeClickable(locator));
    }

    protected List<WebElement> waitForAll(By locator) {
        wait().until(ExpectedConditions.presenceOfAllElementsLocatedBy(locator));
        return driver().findElements(locator);
    }

    protected boolean isElementPresent(By locator) {
        try {
            driver().findElement(locator);
            return true;
        } catch (NoSuchElementException e) {
            return false;
        }
    }

    protected void setViewport(int width, int height) {
        driver().manage().window().setSize(new Dimension(width, height));
    }
}
