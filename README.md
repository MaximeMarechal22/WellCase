# CaseForge - Virtual Case Opening Platform

A complete virtual case opening platform inspired by gaming case opening websites, but 100% free and using only virtual currency.

## Features

- **Case Opening**: Open virtual cases with different tiers and probabilities
- **Inventory System**: Collect and manage your virtual items
- **Upgrade System**: Trade up your items for better ones with calculated success rates
- **Daily Rewards**: Login daily to claim increasing rewards
- **Missions**: Complete tasks to earn bonus virtual currency
- **History**: Track all your openings, upgrades, and rewards
- **Profile**: View your stats and account information
- **Admin Panel**: Manage users, cases, and view statistics (admin only)
- **Virtual Currency**: All transactions use virtual € (no real money involved)

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.14+**: Core programming language
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database for development (can be switched to PostgreSQL/MySQL)
- **Pydantic**: Data validation and settings management
- **JWT**: Authentication token handling

### Frontend
- **React 18**: Modern UI library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API requests
- **Bootstrap 5**: Responsive UI components
- **Vanilla CSS**: Custom styling

## Installation

### Prerequisites
- Python 3.14+
- Node.js 16+ and npm
- Git (optional)

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/caseforge.git
cd caseforge

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Initialize the database
python backend/init_db.py

# Start the backend server
cd backend
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
# In a new terminal
cd frontend

# Install frontend dependencies
npm install

# Start the frontend development server
npm start
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000

### Default Admin Account
- Username: `admin`
- Email: `admin@caseforge.com`
- Password: `admin123`

### Default User Account
- Username: `player1`
- Email: `player1@caseforge.com`
- Password: `player123`

## Project Structure

```
caseforge/
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas for validation
│   │   ├── core/          # Core utilities (security, etc.)
│   │   ├── db/            # Database configuration
│   │   └── main.py        # FastAPI application entry point
│   ├── init_db.py         # Database initialization script
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── public/            # Static assets
│   └── src/
│       ├── components/    # Reusable UI components
│       ├── pages/         # Page components
│       ├── services/      # API service layer
│       ├── contexts/      # React context providers
│       ├── utils/         # Utility functions
│       └── assets/        # Images, icons, etc.
└── README.md              # This file
```

## API Endpoints

### Authentication
- `POST /auth/login` - Login and get access token
- `POST /auth/users/` - Register a new user
- `GET /auth/users/me` - Get current user profile

### Cases
- `GET /cases/` - Get all active cases
- `GET /cases/{id}` - Get specific case details
- `POST /cases/` - Create a new case (admin)
- `PUT /cases/{id}` - Update a case (admin)
- `DELETE /cases/{id}` - Delete a case (admin)

### Items
- `GET /items/` - Get all active items
- `GET /items/{id}` - Get specific item details
- `GET /items/category/{category}` - Get items by category
- `GET /items/rarity/{rarity}` - Get items by rarity
- `POST /items/` - Create a new item (admin)

### Inventory
- `GET /inventory/` - Get user's inventory
- `POST /inventory/` - Add item to inventory
- `DELETE /inventory/{id}` - Remove item from inventory

### Case Openings
- `POST /openings/{case_id}` - Open a case

### Upgrades
- `POST /upgrades/` - Perform an item upgrade

### Daily Rewards
- `GET /daily-rewards/` - Get daily reward status
- `POST /daily-rewards/claim` - Claim daily reward

### Missions
- `GET /missions/` - Get user's missions
- `POST /missions/` - Create a new mission
- `POST /missions/check_case_opening` - Check case opening mission progress
- `POST /missions/check_upgrade` - Check upgrade mission progress

### Dashboard
- `GET /balance` - Get user's virtual balance
- `GET /history` - Get user's transaction history
- `GET /admin/stats` - Get platform statistics (admin)
- `GET /admin/users` - Get all users (admin)
- `GET /admin/cases` - Get all cases (admin)

## Virtual Currency System

All currency in CaseForge is virtual and represented by the € symbol for familiarity, but has **no real-world value**.

- All users start with 10,000 €
- Case openings deduct the case price from your balance
- Wins add the item's virtual value to your balance
- Upgrades have no direct balance cost but consume the original item
- Daily rewards and missions add virtual currency to your balance
- No deposits, withdrawals, or cash-out options exist
- No real money can be deposited, won, or converted

## Security Notes

- All critical calculations (case opening results, upgrade success chances) are performed server-side
- The frontend never determines outcomes or balances
- Virtual currency cannot be converted to real money or transferred between users
- Admin functions are protected by role-based access control

## Customization

### Adding New Cases
1. Add cases through the admin panel or API
2. Define case-item relationships with probabilities
3. Set appropriate pricing based on item values

### Adding New Items
1. Add items through the admin panel or API
2. Assign appropriate rarity, category, and virtual value
3. Provide image URLs or use placeholder images

### Adjusting Probabilities
- Case item probabilities are stored in the `case_items` table
- Probabilities should sum to 100% for each case (normalized automatically)
- Higher rarity items should have lower probabilities

## Future Enhancements

- [ ] Animated case opening sequences
- [ ] Sound effects and music
- [ ] Trade system between users
- [ ] Limited edition cases and items
- [ ] Seasonal events and rewards
- [ ] Improved UI/UX with themes
- [ ] Mobile responsive improvements
- [ ] API rate limiting and enhanced security
- [ ] Docker deployment configuration
- [ ] Comprehensive test suite

## License

This project is open source and available for personal use. Commercial use requires permission.

## Disclaimer

CaseForge is a virtual case opening platform for entertainment purposes only. All items and currency are virtual and have no real-world value. This platform does not constitute gambling and does not offer real money prizes or payouts.

---

Built with ❤️ by the CaseForge Team