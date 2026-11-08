# Jongwa Store - Project Planning

## 1. Project Overview

Jongwa Store is a multi-vendor eCommerce web application developed using Django. The application allows users to register as either vendors or buyers.

Vendors can create and manage their own online stores and sell products. Buyers can browse products from different vendors, add products to their shopping carts, complete purchases and submit product reviews.

The system provides user authentication, role-based access control, stock management, checkout processing, invoice generation and password recovery.

## 2. System Users

### 2.1 Vendors

Vendors can:

- Register and log in.
- Create their own online stores.
- View their registered stores.
- Edit store details.
- Delete their own stores.
- Add products to their stores.
- View, edit and delete their own products.
- Manage product prices and stock quantities.

### 2.2 Buyers

Buyers can:

- Register and log in.
- Browse products from different vendors.
- View product details.
- Add products to their shopping carts.
- Update quantities and remove products from their carts.
- Complete checkout.
- Receive invoices by email.
- Download invoices.
- Submit product reviews.
- View verified and unverified reviews.
- Reset forgotten passwords.

## 3. Functional Requirements

The system must:

1. Allow users to register as buyers or vendors.
2. Authenticate registered users through login and logout.
3. Provide separate permissions for buyers and vendors.
4. Allow vendors to create and manage their own stores.
5. Allow vendors to manage products belonging to their stores.
6. Prevent vendors from accessing or modifying another vendor's stores and products.
7. Allow buyers to browse available products.
8. Provide shopping cart functionality.
9. Validate product stock before checkout.
10. Prevent buyers from purchasing quantities greater than available stock.
11. Deduct product stock after successful checkout.
12. Generate orders and invoices.
13. Email invoices to buyers.
14. Allow buyers to submit product reviews.
15. Identify reviews from buyers with completed purchases as verified.
16. Provide password recovery through email reset links.
17. Expire password reset links after two hours.

## 4. Non-Functional Requirements

### 4.1 Security

- Use Django authentication.
- Implement role-based access control.
- Protect user passwords.
- Use secure password reset tokens.
- Restrict vendors to managing their own stores and products.
- Protect buyer order information.
- Use CSRF protection on forms.

### 4.2 Reliability

- Prevent checkout when the shopping cart is empty.
- Prevent purchases when stock is insufficient.
- Use database transactions during checkout.
- Maintain accurate stock quantities.
- Handle invoice email delivery failures without losing successfully created orders.

### 4.3 Usability

- Provide simple navigation.
- Use clear labels and buttons.
- Display helpful error and success messages.
- Provide separate functionality for buyers and vendors.

### 4.4 Maintainability

- Organise the application using Django's models, views, forms and templates.
- Use reusable components where appropriate.
- Use database migrations to manage database changes.
- Document the application and its requirements.

## 5. Database Requirements

The application uses MariaDB as its relational database.

Django models are used to manage the application's data, including:

- Users and user profiles.
- Stores.
- Products.
- Orders.
- Order items.
- Invoices.
- Product reviews.

Django migrations are used to create and update database tables.

## 6. Technology Requirements

The project uses:

- Python as the programming language.
- Django as the web framework.
- MariaDB as the database management system.
- HTML for page structure.
- CSS for page styling.
- Django authentication for user management.
- ReportLab for PDF invoice generation.
- Email services for invoice and password reset communication.

## 7. Error Handling and Recovery

The system must:

- Validate user input.
- Handle incorrect login details.
- Handle missing stores and products.
- Prevent empty-cart checkout.
- Handle insufficient product stock.
- Handle email delivery failures.
- Prevent unauthorised access.
- Preserve successfully created orders if invoice email delivery fails.
- Provide clear messages when an operation cannot be completed.

## 8. Project Security and Data Protection

The application uses authentication and role-based permissions to protect its functionality.

Vendors can only manage stores and products that belong to them. Buyers cannot access vendor management functionality.

The application also uses Django's password hashing and secure password reset functionality to protect user accounts.

## 9. Project Objectives

The main objectives of Jongwa Store are to:

- Provide a platform for multiple vendors to sell products.
- Allow buyers to shop from different vendors.
- Provide secure user registration and authentication.
- Support online shopping cart and checkout functionality.
- Maintain accurate product stock.
- Generate and deliver purchase invoices.
- Allow buyers to share product feedback.

## 10. Conclusion

Jongwa Store aims to provide a secure and user-friendly multi-vendor eCommerce platform. The application combines vendor management, product browsing, shopping cart functionality, checkout processing, invoicing and product reviews in one system.