@blog
Feature: Blog Tab - EPAM SolutionsHub
  As a visitor of EPAM SolutionsHub
  I want to browse and read Blog posts
  So that I can stay informed about EPAM's latest insights and articles

  Background:
    Given the user navigates to the Blog page

  @smoke @TC-BLG-001
  Scenario: Blog page loads successfully
    Then the page should load with HTTP status 200
    And blog posts should be displayed with title, date, and teaser text

  @smoke @TC-BLG-002
  Scenario: Blog tab is highlighted as active in navigation
    When the user inspects the main navigation bar
    Then the "Blog" menu item should be highlighted as the active tab

  @smoke @TC-BLG-003
  Scenario: Clicking a blog post title opens the full article
    Given at least one blog post is visible in the listing
    When the user clicks on the first blog post title
    Then the full article page should load
    And the article should display the author name
    And the article should display the publication date
    And the full article content should be visible

  @regression @TC-BLG-004
  Scenario: All images in a blog article load without errors
    Given the user is on a blog article page
    Then all images on the page should render without broken image icons
    And all images should have alt text attributes

  @regression @TC-BLG-005
  Scenario: Blog posts are sorted by date with the newest post first
    When the user views the blog listing
    Then the blog posts should be displayed in descending date order
    And the first post should have a date equal to or newer than the second post

  @regression @TC-BLG-006
  Scenario: Pagination works on the Blog listing
    Given the blog listing has more posts than fit on one page
    When the user scrolls to the bottom of the Blog page
    And the user clicks the next page control
    Then the next set of blog posts should be loaded
    And the page state or URL should update to reflect the new page

  @regression @TC-BLG-007
  Scenario: Back navigation from article returns to Blog listing
    Given the user has opened a blog article
    When the user clicks the browser back button
    Then the user should be returned to the Blog listing page
    And the Blog listing content should be visible

  @responsive @TC-BLG-008
  Scenario Outline: Blog page is responsive on different viewports
    Given the browser viewport is set to width "<width>" and height "<height>"
    When the user navigates to the Blog page
    Then the blog listing should display without horizontal scrolling on "<device>"
    And opening an article should render the full content readably

    Examples:
      | device | width | height |
      | mobile | 375   | 812    |
      | tablet | 768   | 1024   |
