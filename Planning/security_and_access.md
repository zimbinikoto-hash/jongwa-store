# Jongwa Store - Security and Access Control

## 1. User Authentication

The application uses Django's built-in authentication system to manage user accounts.

Security measures include:

- Require users to register and log in.
- Allow users to log out securely.
- Use Django password hashing to protect passwords.
- Provide password recovery through email.
- Use secure password reset tokens.
- Set password reset links to expire after two hours.
- Prevent unauthenticated users from accessing protected views.

## 2. User Roles

The application supports two user roles: vendors and buyers.

### 2.1 Vendors

Vendors can:

- Create and manage their own stores.
- View their registered stores.
- Edit their own store details.
- Delete their own stores.
- Add products to their stores.
- View, edit and delete their own products.
- Manage product prices and stock quantities.

Vendors cannot modify or delete stores and products belonging to other vendors.

### 2.2 Buyers

Buyers can:

- Browse available products.
- View product details.
- Manage their shopping carts.
- Place orders.
- Receive invoices.
- Submit product reviews.
- View verified and unverified reviews.
- Access their own order information.

Buyers cannot access vendor management functionality.

## 3. Data Protection

The application uses the following data protection measures:

- Store passwords using Django's password hashing.
- Use CSRF protection on forms.
- Validate user input.
- Use Django ORM to interact with the database.
- Protect sensitive user information.
- Restrict access to private information.
- Use environment variables to store email credentials rather than hardcoding them in application code.

## 4. Permissions and Access Control

The application uses Django authentication and role-based permissions to control access to protected functionality.

Security measures include:

- Use Django's `login_required` decorators.
- Check user roles before granting access to vendor functionality.
- Verify ownership before allowing changes to stores and products.
- Restrict vendors to managing their own stores and products.
- Prevent buyers from accessing vendor dashboards.
- Return a 404 response when a user attempts to access another vendor's protected store or product pages.

Ownership is checked at the database query