Feature: Initialize a Paychex session
  Scenario: Initialize a Paychex session
    Given I create a Paychex object
    And I call the initialize_session method
    Then the Paychex object contains the necessary session state

  Scenario: A brand new Paychex object does not have the needed session state
    Given I create a Paychex object
    Then the Paychex object does not contain the necessary session state
