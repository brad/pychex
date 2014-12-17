Feature: Get the 401k information
  Scenario: Get the 401k information
    Given I create a Paychex object
    And I call the post_username method
    And I call the login method
    And I call the get_account_summary method
    Then the Paychex object contains an app_username member variable with the correct value
    And while mocking, the Paychex object contains a current_balance member variable set to "$XX,XXX.XX"
    And while mocking, the Paychex object contains a vested_balance member variable set to "$XX,XXX.XX"
    And while mocking, the Paychex object contains a personal_ror member variable set to "X.X%"
    And the Paychex object contains a balance_tab_info member variable with the following data:
      | percent | symbol | fund                                                                                      | shares  | balance    | prospectus                                              |
      | 9.79    | FNAMW  | {"name": "FAKE NAME W", "url": "http://www.example.com/?product=FUNDS&custno=1&FUNDID=1"} | 103.572 | $6,644.72  | http://www.example.com/?product=PROSP&custno=1&FUNDID=1 |
      | 10.21   | FNAMX  | {"name": "FAKE NAME X", "url": "http://www.example.com/?product=FUNDS&custno=1&FUNDID=2"} | 214.321 | $6,929.78  | http://www.example.com/?product=PROSP&custno=1&FUNDID=2 |
      | 31.58   | FNAMY  | {"name": "FAKE NAME Y", "url": "http://www.example.com/?product=FUNDS&custno=1&FUNDID=3"} | 13.179  | $21,434.13 | http://www.example.com/?product=PROSP&custno=1&FUNDID=3 |
      | 48.42   | FNAMZ  | {"name": "FAKE NAME Z", "url": "http://www.example.com/?product=FUNDS&custno=1&FUNDID=4"} | 26.624  | $32,863.86 | http://www.example.com/?product=PROSP&custno=1&FUNDID=4 |

  Scenario: Try to get the 401k information without logging in
    Given I create a Paychex object
    And I call the get_account_summary method
    Then the Paychex object contains a logged_in member variable set to False
    Then the Paychex object contains a app_username member variable set to None
    And the Paychex object contains a current_balance member variable set to None
    And the Paychex object contains a vested_balance member variable set to None
    And the Paychex object contains a personal_ror member variable set to None
    And the Paychex object contains a balance_tab_info member variable set to None
    And we have raised an exception:PychexUnauthenticatedError
