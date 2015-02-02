Feature: Initialize a Paychex object
  Scenario: Initialize a Paychex object with username only
    Given I create a Paychex object
    Then the Paychex object contains the needed urls
    And the Paychex object contains content-type shortcuts
    And the Paychex object contains a session
    And the Paychex object contains a logged_in member variable set to False
    And the Paychex object contains a security_image_path member variable set to None

  Scenario: Initialize a Paychex object with username and security image
    Given I create a Paychex object with username and security image
    Then the Paychex object contains the needed urls
    And the Paychex object contains content-type shortcuts
    And the Paychex object contains a session
    And the Paychex object contains a logged_in member variable set to False
    And the Paychex object contains the correct security image path
    And the get_security_image method returns the full security image url

  Scenario: Initialize a BenefitsOnline object
    Given I create a BenefitsOnline object
    Then the BenefitsOnline object contains the needed urls
    And the BenefitsOnline object contains a session
    And the BenefitsOnline object contains a logged_in member variable set to False
    And the BenefitsOnline object contains a retirement_services member variable set to None

  Scenario: Initialize a RetirementServices object
    Given I create a BenefitsOnline object
    And I call the BenefitsOnline.login method
    Then the RetirementServices object contains the needed urls
    And the RetirementServices object contains a session
    And the RetirementServices object contains a logged_in member variable set to False
    And the RetirementServices object contains a current_balance member variable set to None
    And the RetirementServices object contains a vested_balance member variable set to None
    And the RetirementServices object contains a personal_ror member variable set to None
    And the RetirementServices object contains a balance_tab_info member variable set to None
