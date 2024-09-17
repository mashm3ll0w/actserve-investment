# Actserve Investment App
An app for managing investment accounts

# Project Requirements

Create a Django Rest Framework (DRF) API for managing investment accounts that allows more than one user to belong to an investment account it should also allow a user to belong to more than one investment account, with the following requirements:
- [ ] User Permissions: Extend the User and Django model permissions so that a user can have multiple investment accounts, each with different levels of access:
- [ ] Investment Account 1: The user should only have view rights and should not be able to make transactions.
- [ ] Investment Account 2: The user should have full CRUD (Create, Read, Update, Delete) permissions.
- [ ] Investment Account 3: The user should only be able to post transactions, but not view them.
- [ ] Admin Endpoint: Create an admin endpoint that returns all of a user's transactions, along with a nested sum of the user's total balance. Additionally, this endpoint should include a date range filter to retrieve transactions that occurred within a specified date range.
- [ ] Unit Tests: Write unit tests to validate the functionality of the APIs.
- [ ] GitHub Action: Set up a GitHub Action to automatically run the unit tests.