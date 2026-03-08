@solutions
Feature: Solutions Tab - EPAM SolutionsHub
  As a visitor of EPAM SolutionsHub
  I want to browse and filter the Solutions catalog
  So that I can find relevant software solutions for my needs

  Background:
    Given the user navigates to the Solutions catalog page

  @smoke @TC-SOL-001
  Scenario: Solutions page loads successfully
    Then the page should load with HTTP status 200
    And the solutions catalog should be displayed
    And no JavaScript console errors should be present

  @smoke @TC-SOL-002
  Scenario: Solutions tab is highlighted as active in navigation
    When the user inspects the main navigation bar
    Then the "Solutions" menu item should be highlighted as the active tab

  @regression @TC-SOL-003
  Scenario Outline: Filtering solutions by Industry
    When the user selects the Industry filter "<industry>"
    Then the catalog should update to show only solutions tagged with "<industry>"
    And the active filter chip "<industry>" should be visible

    Examples:
      | industry        |
      | Healthcare      |
      | Financial Services |
      | EdTech          |
      | Retail & CPG    |

  @regression @TC-SOL-004
  Scenario: Multiple filters can be applied simultaneously
    When the user selects the Industry filter "Healthcare"
    And the user selects the Category filter "Artificial Intelligence"
    Then the catalog should display results matching both filters
    And the active filter chips should show "Healthcare" and "Artificial Intelligence"

  @regression @TC-SOL-005
  Scenario: Clearing all filters restores the full catalog
    Given the user has applied the Industry filter "Healthcare"
    When the user clicks the "Clear All" filters button
    Then the full solutions catalog should be restored
    And no active filter chips should be visible

  @regression @TC-SOL-006
  Scenario: Search functionality filters solutions by keyword
    When the user types "healthcare" in the search bar
    Then the catalog should filter to show only solutions related to "healthcare"
    And the displayed results should be relevant to the search term

  @regression @TC-SOL-007
  Scenario: No results state is shown for an invalid search term
    When the user types "zzzyyyxxx" in the search bar
    Then an empty state message should be displayed
    And the page should not crash or show any errors

  @smoke @TC-SOL-008
  Scenario: Clicking a solution card navigates to the detail page
    Given at least one solution card is visible in the catalog
    When the user clicks on the first solution card
    Then the user should be navigated to the solution detail page
    And the page URL should change to reflect the selected solution
    And the solution detail content should be loaded

  @regression @TC-SOL-009
  Scenario: Solution detail page displays all required content
    Given the user is on a solution detail page
    Then the detail page should display the solution title
    And the detail page should display the solution description
    And the detail page should display solution tags or category
    And the detail page should display relevant action buttons

  @responsive @TC-SOL-010
  Scenario Outline: Solutions page is responsive on different viewports
    Given the browser viewport is set to width "<width>" and height "<height>"
    When the user navigates to the Solutions catalog page
    Then all page elements should be visible without horizontal scrolling
    And the filter panel should adapt to the "<device>" layout
    And solution cards should be properly displayed

    Examples:
      | device  | width | height |
      | mobile  | 375   | 812    |
      | tablet  | 768   | 1024   |
      | desktop | 1920  | 1080   |
