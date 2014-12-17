Feature: Login to Paychex
  Scenario: Login to Paychex
    Given I create a Paychex object
    And I call the post_username method
    And I call the login method
    Then the Paychex object contains the necessary session state
    And the Paychex object contains the correct security image path
    And the Paychex object contains a logged_in member variable set to True

  Scenario: Login to Paychex with pre-set security image
    Given I create a Paychex object with username and security image
    And I call the post_username method
    And I call the login method
    Then the Paychex object contains the necessary session state
    And the Paychex object contains the correct security image path
    And the Paychex object contains a logged_in member variable set to True

  Scenario: Fail login to Paychex with invalid password
    Given I create a Paychex object
    And I call the post_username method
    And I call the login method with the wrong password
    Then the Paychex object contains the necessary session state
    And the Paychex object contains the correct security image path
    And the Paychex object contains a logged_in member variable set to False
    And we have raised an exception:PychexInvalidPasswordError

  Scenario: Fail login to Paychex because we haven't posted the username yet
    Given I create a Paychex object
    And I call the login method
    Then the Paychex object does not contain the necessary session state
    And the Paychex object contains a security_image_path member variable set to None
    And the Paychex object contains a logged_in member variable set to False
    And we have raised an exception:PychexSecurityImageMissingError
