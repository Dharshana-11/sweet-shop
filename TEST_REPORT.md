# Test Report

## Test Command

```bash
python manage.py test
```

## Test Output

```text
Found 16 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
................
----------------------------------------------------------------------
Ran 16 tests in 36.713s

OK
Destroying test database for alias 'default'...
```

## Summary

- Total Tests: 16
- Result: All tests passed

## Coverage

The test suite validates the following backend functionalities:

### Authentication & Authorization

- User registration via the register endpoint
- User login with valid credentials
- Login failure with invalid credentials
- JWT token generation on successful login
- Access restriction for unauthenticated users on protected endpoints

### Sweets Management (CRUD)

- Listing sweets requires authentication
- Creating a new sweet as an authenticated user
- Updating an existing sweet with valid authentication
- Preventing unauthorized users from accessing protected sweet APIs

### Search & Filtering

- Searching sweets by category
- Searching sweets using price range filters
- Ensuring only matching records are returned

### Role-Based Access Control

- Restricting delete operations to admin users only
- Preventing non-admin users from deleting sweets
- Restricting restock functionality to admin users

### Inventory Operations

- Purchasing a sweet decreases available quantity
- Preventing purchase when a sweet is out of stock
- Restocking sweets increases inventory count
- Validating restock input and rejecting invalid requests
