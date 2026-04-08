@bdd @mvp
Feature: Authentication
  Scenario: Successful login with valid credentials
    Given an active user with email "admin@ideas.com" and password "ChangeMe123!"
    When I submit POST "/api/v1/auth/login" with those credentials
    Then the response status should be 200
    And the response should include "access_token"
