Feature: Get the Benefits OnLine app username
  Scenario: Get the Benefits OnLine app username
    Given I create a Paychex object
    And I call the post_username method
    And I call the Paychex.login method
    Then the get_bol_username method returns the correct bol_username

  Scenario: Try to get the Benefits OnLine app username without logging in
    Given I create a Paychex object
    And I call the get_bol_username method
    And we have raised an exception:PychexUnauthenticatedError

  Scenario: Try to get the Benefits OnLine app username when a user has no BOL account
    Given I create a Paychex object
    And I call the post_username method
    And I call the Paychex.login method
    And I call the get_bol_username method with no BOL account
    Then while mocking, we have raised an exception:PychexNoBolUsernameError
