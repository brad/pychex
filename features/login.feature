Feature: Login to Paychex
  Scenario: Login to Paychex
    Given I create a Paychex object
    And I call the post_username method
    And I call the Paychex.login method
    Then the Paychex object contains the necessary session state
    And the Paychex object contains the correct security image path
    And the Paychex object contains a logged_in member variable set to True

  Scenario: Login to Paychex with pre-set security image
    Given I create a Paychex object with username and security image
    And I call the post_username method
    And I call the Paychex.login method
    Then the Paychex object contains the necessary session state
    And the Paychex object contains the correct security image path
    And the Paychex object contains a logged_in member variable set to True

  Scenario: Fail login to Paychex with invalid password
    Given I create a Paychex object
    And I call the post_username method
    And I call the Paychex.login method with the wrong password
    Then the Paychex object contains the necessary session state
    And the Paychex object contains the correct security image path
    And the Paychex object contains a logged_in member variable set to False
    And we have raised an exception:PychexInvalidPasswordError

  Scenario: Fail login to Paychex because we haven't posted the username yet
    Given I create a Paychex object
    And I call the Paychex.login method
    Then the Paychex object does not contain the necessary session state
    And the Paychex object contains a security_image_path member variable set to None
    And the Paychex object contains a logged_in member variable set to False
    And we have raised an exception:PychexSecurityImageMissingError

  Scenario: Login to Benefits Online
    Given I create a BenefitsOnline object
    And I call the BenefitsOnline.login method
    Then the BenefitsOnline object contains a logged_in member variable set to True
    And the BenefitsOnline object contains a retirement_services member variable of type:RetirementServices

  Scenario: Fail login to Benefits Online with invalid password
    Given I create a BenefitsOnline object
    And I call the BenefitsOnline.login method with the wrong password
    Then the BenefitsOnline object contains a logged_in member variable set to False
    And the BenefitsOnline object contains a retirement_services member variable set to None
    And we have raised an exception:PychexInvalidPasswordError

  Scenario: Login to Retirement Services
    Given I create a BenefitsOnline object
    And I call the BenefitsOnline.login method
    And I call the RetirementServices.login method
    Then the RetirementServices object contains a logged_in member variable set to True

  Scenario: Fail login to RetirementServices with unknown error
    Given I create a BenefitsOnline object
    And I call the BenefitsOnline.login method
    And I get an error logging in to Retirement Services
    Then the RetirementServices object contains a logged_in member variable set to False
    And we have raised an exception:PychexUnknownError
