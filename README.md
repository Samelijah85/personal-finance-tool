
---

# Personal Finance Management Tool

A full-stack application that helps users manage their personal finances by tracking transactions, creating budgets, and generating financial summaries.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Architecture](#project-architecture)
- [Setup Instructions](#setup-instructions)
- [Usage Guidelines](#usage-guidelines)
- [API Endpoints](#api-endpoints)
- [Next Steps](#next-steps)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

The Personal Finance Management Tool is designed to help users track their finances through detailed transaction logs and budgeting features. Users can register, log in, and securely manage their personal financial data. The tool provides an intuitive frontend built with Vue.js, communicating with a backend powered by FastAPI.

---

## Features
- **User Authentication**: JWT-based login and registration.
- **Transaction Management**: Add, edit, view, and delete personal financial transactions.
- **Budget Management**: Create and manage budgets, associate them with transactions.
- **Financial Summary Reports**: Generate a summary report of all transactions.
- **Responsive UI**: The frontend is designed to work seamlessly across devices.

---

## Technologies Used

### Backend:
- **FastAPI**: High-performance, modern API framework.
- **PyMongo**: MongoDB integration for data storage.
- **PyJWT**: Secure authentication using JWT tokens.
- **Passlib**: Password hashing for user security.
- **Pydantic**: Data validation and serialization.

### Frontend:
- **Vue.js**: Progressive JavaScript framework for building user interfaces.
- **Vuetify**: Material Design component framework for Vue.js.
- **Axios**: Promise-based HTTP client for API requests.
- **Vue Router**: Client-side routing.

### Dev Tools:
- **Vite**: Next-generation frontend build tool.
- **ESLint**: Linting tool for identifying and fixing problems in JavaScript code.
- **Prettier**: Code formatting tool for consistent style.

---

## Project Architecture

The project follows a modular architecture with a clear separation of concerns between the frontend and backend.

- **Backend**: 
  - Built using FastAPI with a RESTful API.
  - MongoDB serves as the primary data storage system.
  - JWT-based authentication secures access to the application.
  
- **Frontend**: 
  - Built with Vue.js, utilizing Vuetify for a modern UI.
  - Axios handles HTTP requests to communicate with the backend API.
  - Vue Router provides dynamic navigation between components.

---

## Setup Instructions

### Prerequisites:
- **Python 3.8+** for backend
- **Node.js 16+** for frontend
- **MongoDB** installed or accessible remotely

### Backend Setup (FastAPI)

1. Clone the repository:
   ```bash
   git clone https://github.com/Samelijah85/personal-finance-tool.git
   cd personal-finance-tool/backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables in a `.env` file:
   ```bash
   SECRET_KEY=your_jwt_secret_key
   MONGO_URI=mongodb://localhost:27017/your-db-name
   ```

5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup (Vue.js)

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173` to view the app.

---

## Usage Guidelines

1. **Register a new user**:
   - Go to the registration page and create a new account. You’ll receive a JWT token upon successful registration.
   
2. **Login**:
   - Use your credentials to log in and obtain a JWT token. The token will be required for subsequent API calls to manage transactions and budgets.
   
3. **Managing Transactions**:
   - Add, edit, or delete transactions using the transaction management UI.
   
4. **Setting Budgets**:
   - Create and manage budgets, and associate them with your transactions.
   
5. **Viewing Summary Reports**:
   - Navigate to the reports page to view a summary of all your transactions.

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user.
- `POST /api/v1/auth/login` - Log in to the system.

### Transactions
- `GET /api/v1/transactions/` - Retrieve all transactions.
- `POST /api/v1/transactions/` - Add a new transaction.
- `GET /api/v1/transactions/{id}` - Retrieve a specific transaction.
- `PUT /api/v1/transactions/{id}` - Update a transaction.
- `DELETE /api/v1/transactions/{id}` - Delete a transaction.

### Budgets
- `GET /api/v1/budgets/` - Retrieve all budgets.
- `POST /api/v1/budgets/` - Add a new budget.
- `GET /api/v1/budgets/{id}` - Retrieve a specific budget.
- `PUT /api/v1/budgets/{id}` - Update a budget.
- `DELETE /api/v1/budgets/{id}` - Delete a budget.

### Reports
- `GET /api/v1/reports/summary` - Retrieve a summary report of all transactions.

---

## Next Steps

- **Advanced Reporting**: Add visual charts and graphs for financial reports.
- **Role-Based Access Control**: Implement user roles (admin, regular users).
- **Deployment**: Deploy to cloud platforms (e.g., AWS, Heroku, DigitalOcean).

---

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
