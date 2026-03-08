@guides
Feature: Guides Tab - EPAM SolutionsHub
  As a visitor of EPAM SolutionsHub
  I want to browse and read Guides
  So that I can learn about topics relevant to software engineering

  Background:
    Given the user navigates to the Guides page

  @smoke @TC-GUI-001
  Scenario: Guides page loads successfully
    Then the page should load with HTTP status 200
    And a list of guides should be displayed with titles and summaries

  @smoke @TC-GUI-002
  Scenario: Guides tab is highlighted as active in navigation
    When the user inspects the main navigation bar
    Then the "Guides" menu item should be highlighted as the active tab

  @smoke @TC-GUI-003
  Scenario: Clicking a guide card navigates to the guide detail page
    Given at least one guide is visible in the listing
    When the user clicks on the first guide card
    Then the guide detail page should open
    And the full guide content should be displayed with proper formatting

  @regression @TC-GUI-004
  Scenario: Guide detail page content is properly formatted
    Given the user is on a guide detail page
    Then the guide should display headings with correct styling
    And the guide text should be readable
    And all guide images should load without errors

  @regression @TC-GUI-005
  Scenario: Back navigation from guide returns to the Guides listing
    Given the user is on a guide detail page
    When the user clicks the browser back button
    Then the user should be returned to the Guides listing page
    And the Guides listing content should be visible

  @responsive @TC-GUI-006
  Scenario Outline: Guides page is responsive on different viewports
    Given the browser viewport is set to width "<width>" and height "<height>"
    When the user navigates to the Guides page
    Then the guide listing should be readable on the "<device>" layout
    And clicking into a guide should display readable content without horizontal scroll

    Examples:
      | device | width | height |
      | mobile | 375   | 812    |
      | tablet | 768   | 1024   |
