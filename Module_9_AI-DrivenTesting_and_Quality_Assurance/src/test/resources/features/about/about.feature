@about
Feature: About Tab - EPAM SolutionsHub
  As a visitor of EPAM SolutionsHub
  I want to view the About page
  So that I can learn about EPAM and how to get in contact

  Background:
    Given the user navigates to the About page

  @smoke @TC-ABT-001
  Scenario: About page loads successfully
    Then the page should load with HTTP status 200
    And all About page content sections should be visible

  @smoke @TC-ABT-002
  Scenario: About tab is highlighted as active in navigation
    When the user inspects the main navigation bar
    Then the "About" menu item should be highlighted as the active tab

  @regression @TC-ABT-003
  Scenario: All internal links on the About page are functional
    When the user collects all internal links on the About page
    Then each internal link should return HTTP status 200
    And no link should lead to a 404 page

  @regression @TC-ABT-004
  Scenario: External links open in a new browser tab
    When the user clicks an external link on the About page
    Then a new browser tab should be opened
    And the original About page should remain open in the previous tab

  @smoke @TC-ABT-005
  Scenario: Contact Us button is clickable and functional
    Given the "Contact Us" button is present on the About page
    When the user clicks the "Contact Us" button
    Then a contact form or modal should be displayed
    And no JavaScript errors should occur

  @regression @TC-ABT-006
  Scenario: All images on the About page load correctly
    When the user inspects all images on the About page
    Then all images should render without broken image icons
    And all images should be appropriately sized within their containers

  @regression @TC-ABT-007
  Scenario: About page content is complete
    Then the About page should display the company description
    And the About page should display the company mission or purpose statement
    And key informational sections should be present and populated

  @responsive @TC-ABT-008
  Scenario Outline: About page is responsive on different viewports
    Given the browser viewport is set to width "<width>" and height "<height>"
    When the user navigates to the About page
    Then all sections should be readable without horizontal overflow on "<device>"
    And all buttons should be tappable or clickable

    Examples:
      | device | width | height |
      | mobile | 375   | 812    |
      | tablet | 768   | 1024   |
