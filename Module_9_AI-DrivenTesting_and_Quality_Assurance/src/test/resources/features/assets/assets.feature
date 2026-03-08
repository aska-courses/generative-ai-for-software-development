@assets
Feature: Assets Tab - EPAM SolutionsHub
  As a visitor of EPAM SolutionsHub
  I want to browse and filter the Assets catalog
  So that I can find relevant methods, templates, and beta solutions

  Background:
    Given the user navigates to the Assets catalog page

  @smoke @TC-ASS-001
  Scenario: Assets page loads successfully
    Then the page should load with HTTP status 200
    And the assets catalog should be displayed

  @smoke @TC-ASS-002
  Scenario: Assets tab is highlighted as active in navigation
    When the user inspects the main navigation bar
    Then the "Assets" menu item should be highlighted as the active tab

  @regression @TC-ASS-003
  Scenario Outline: Filtering assets by Competency Center
    When the user selects the Competency Center filter "<center>"
    Then the asset list should update to show only assets under "<center>"

    Examples:
      | center            |
      | Testing           |
      | AI/ML Capabilities|
      | Mobile            |
      | Business Analysis |

  @regression @TC-ASS-004
  Scenario Outline: Filtering assets by Asset Type
    When the user selects the Asset Type filter "<type>"
    Then only assets of type "<type>" should be displayed

    Examples:
      | type                |
      | Method & Template   |
      | Beta solution       |

  @regression @TC-ASS-005
  Scenario: Combining Type and Competency Center filters
    When the user selects the Asset Type filter "Beta solution"
    And the user selects the Competency Center filter "AI/ML Capabilities"
    Then the results should be filtered by both "Beta solution" and "AI/ML Capabilities"
    And either relevant assets are displayed or an empty state message is shown

  @smoke @TC-ASS-006
  Scenario: Clicking an asset card opens the detail page
    Given at least one asset card is visible in the catalog
    When the user clicks on the first asset card
    Then the asset detail page should load
    And the full asset description and metadata should be visible

  @regression @TC-ASS-007
  Scenario: Search within Assets returns relevant results
    When the user types "automation" in the search bar
    Then the asset list should filter to show automation-related assets
    And the displayed results should be relevant to "automation"

  @regression @TC-ASS-008
  Scenario: Empty state is shown when no assets match the search
    When the user types "zzzyyyxxx" in the search bar
    Then an empty state or no-results message should be displayed
    And no JavaScript errors should occur

  @responsive @TC-ASS-009
  Scenario Outline: Assets page is responsive on different viewports
    Given the browser viewport is set to width "<width>" and height "<height>"
    When the user navigates to the Assets catalog page
    Then all page elements should be visible without horizontal scrolling
    And filters and asset cards should be usable on the "<device>" layout

    Examples:
      | device | width | height |
      | mobile | 375   | 812    |
      | tablet | 768   | 1024   |
