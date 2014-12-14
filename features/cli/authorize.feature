Feature: Authorize to Paychex
  Scenario: Authorize to Paychex
    Given I run the authorize command
    Then the pychex.cfg file should contain the encrypted credentials
