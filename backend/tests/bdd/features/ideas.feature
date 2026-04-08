@bdd @mvp
Feature: Ideas
  Scenario: Authenticated user can create and list ideas
    Given I am authenticated as "admin@ideas.com" with password "ChangeMe123!"
    When I create an idea with title "BDD Idea" and description "BDD Description"
    Then the response status should be 201
    And the created idea should have owner and status
    When I list my ideas
    Then the response status should be 200
    And the ideas list should contain title "BDD Idea"
