Feature: Post a Paychex username
  Scenario: Post a Paychex username
    Given I create a Paychex object
    And I call the post_username method
    Then the Paychex object contains the necessary session state
    And the Paychex object contains the correct security image path
    And the get_security_image method returns the full security image url
    And the Paychex object contains a logged_in member variable set to False

  Scenario: Post a Paychex username on an object with pre-set security image
    Given I create a Paychex object with username and security image
    And I call the post_username method
    Then the Paychex object contains the necessary session state
    And we have raised no exceptions
    And the get_security_image method returns the full security image url
    And the Paychex object contains a logged_in member variable set to False

  Scenario: Post a Paychex username on an object with the wrong security image
    Given I create a Paychex object with username and the wrong security image
    And I call the post_username method
    Then the Paychex object contains the necessary session state
    And we have raised an exception:PychexSecurityImageMismatchError
    And the Paychex object contains a logged_in member variable set to False

  Scenario: Try call get_security_image before post_username
    Given I create a Paychex object
    And I call the get_security_image method
    Then we have raised an exception:PychexSecurityImageMissingError
