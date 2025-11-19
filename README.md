This is a Python CLI variant of my own personal budget sheet, designed in such a way where two people's finances are tracked and calculated in a way for both parties to have a "balanced" plan so that everyone can get the bills paid while also having money for themselves.

In it's current state, I still prefer to use my spreadsheet to do all this until I can come up with a GUI that is easier to use than a spreadsheet.

This is not financial advice.

CURRENT ISSUES/PLANS

- BUG: When a person doesn't have any expenses of their own, they do not seem to appear in Expense Plan print-out
- FEATURE: Establish a People class and have Cashflows associated to People, rather than directly to the Expense Plan. Expense Plan should combine the Cashflows of People, respectfully.
- FEATURE: Offer flexibility to Pay Periods - ability to select between Weekly(ABCD), Biweekly (A/B), or Monthly formatting when printing a plan out.
- FEATURE: Need a way for the Expense Plan to automatically convert pay periods of all cashflows when the pay period selector is changed.
- FEATURE: Offer a way to change currency symbol