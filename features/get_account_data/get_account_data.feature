Feature: Get the Benefits OnLine app username
  Scenario: Get the Benefits OnLine app username
    Given I create a Paychex object
    And I call the post_username method
    And I call the login method
    And I call the get_account_data method
    Then the Paychex object contains an app_username member variable with the correct value

  Scenario: Try to get the Benefits OnLine app username without logging in
    Given I create a Paychex object
    And I call the get_account_data method
    Then the Paychex object contains a logged_in member variable set to False
    Then the Paychex object contains a app_username member variable set to None
    And we have raised an exception:PychexUnauthenticatedError

  Scenario: Try to get the Benefits OnLine app username when a user has no BOL account
    Given I create a Paychex object
    And I call the post_username method
    And I call the login method
    And I call the get_account_data method with no BOL account
    Then the Paychex object contains a logged_in member variable set to True
    Then the Paychex object contains a app_username member variable set to None while mocking
    And we have raised an exception:PychexNoAppUsernameError while mocking
