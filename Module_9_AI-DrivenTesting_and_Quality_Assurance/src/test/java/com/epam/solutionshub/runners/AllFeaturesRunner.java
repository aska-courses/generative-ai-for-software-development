package com.epam.solutionshub.runners;

import org.junit.platform.suite.api.*;

/**
 * Main test suite runner – executes ALL feature files.
 *
 * Run all tests:       ./gradlew test
 * Run smoke tests:     ./gradlew test -Dcucumber.filter.tags="@smoke"
 * Run by tab:          ./gradlew test -Dcucumber.filter.tags="@solutions"
 * Run responsive only: ./gradlew test -Dcucumber.filter.tags="@responsive"
 *
 * Available tags: @smoke, @regression, @responsive, @wip
 *                 @solutions, @assets, @guides, @blog, @about
 */
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(
        key   = "cucumber.glue",
        value = "com.epam.solutionshub.steps,com.epam.solutionshub.hooks"
)
@ConfigurationParameter(
        key   = "cucumber.plugin",
        value = "pretty,html:build/reports/cucumber/report.html,json:build/reports/cucumber/report.json"
)
public class AllFeaturesRunner {
    // JUnit Platform Suite – no body required
}
