# Financial Management System - User Guide

## 🚀 Application Running Successfully!

Your Madrasha Management System is now running on: **http://127.0.0.1:5000**

---

## 🔑 Login Credentials

### Admin/Super User
- **Phone**: 01712345678
- **Password**: admin123
- **Role**: Super User (Full Access)

### Teacher
- **Phone**: 01812345678
- **Password**: teacher123
- **Role**: Teacher

### Student
- **Phone**: 01912345678
- **Password**: student123
- **Role**: Student

---

## 💰 Fee Management System

The financial/accounting system is accessible through the `/api/fees` endpoints.

### Available Features

#### 1. **Load Monthly Fees**
View all fees for a specific batch and year.

**Endpoint**: `GET /api/fees/load-monthly`

**Parameters**:
- `batch_id` (required): The ID of the batch
- `year` (optional): The year (defaults to current year)

**Example**:
```bash
curl "http://127.0.0.1:5000/api/fees/load-monthly?batch_id=1&year=2025"
```

**Response**: Returns all students in the batch with their fee status for each month (1-12).

#### 2. **Save Monthly Fee**
Create or update a fee entry for a student.

**Endpoint**: `POST /api/fees/save-monthly`

**Request Body**:
```json
{
  "student_id": 1,
  "batch_id": 1,
  "month": 4,
  "year": 2025,
  "amount": 1500
}
```

**Example**:
```bash
curl -X POST http://127.0.0.1:5000/api/fees/save-monthly \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "batch_id": 1,
    "month": 4,
    "year": 2025,
    "amount": 1500
  }'
```

**Features**:
- Creates new fee if it doesn't exist
- Updates existing fee if found
- Deletes fee if amount is set to 0
- Automatically sets due date to last day of the month
- Validates student enrollment in batch

#### 3. **Test Endpoint**
Verify that the fee routes are working.

**Endpoint**: `GET /api/fees/test`

**Example**:
```bash
curl http://127.0.0.1:5000/api/fees/test
```

---

## 📊 Current Test Data

### Batches
1. **HSC 2025 - Physics** (ID: 1)
   - Fee Amount: 1500 Taka/month
   - Status: Active

2. **HSC 2025 - Chemistry** (ID: 2)
   - Fee Amount: 1200 Taka/month
   - Status: Active

### Student Enrollment
- **Sample Student** (Phone: 01912345678)
  - Enrolled in: HSC 2025 - Physics
  
### Sample Fees
- **January 2025**: 1500 Taka - ✅ PAID (Paid on: 2025-01-15)
- **February 2025**: 1500 Taka - ⏳ PENDING
- **March 2025**: 1500 Taka - ⚠️ OVERDUE (Late Fee: 100 Taka)

---

## 🗄️ Database Structure

### Fee Table Fields
- `id`: Unique fee identifier
- `user_id`: Student ID
- `batch_id`: Batch ID
- `amount`: Fee amount (decimal)
- `due_date`: Payment due date
- `paid_date`: Date when payment was made
- `status`: Fee status (PENDING, PAID, OVERDUE)
- `payment_method`: How the payment was made (Cash, Bank Transfer, etc.)
- `transaction_id`: Reference number for the transaction
- `late_fee`: Additional late payment fee
- `discount`: Any discount applied
- `notes`: Additional notes about the fee
- `created_at`: When the fee was created
- `updated_at`: Last update timestamp

### Fee Status Values
- **PENDING**: Payment not yet received
- **PAID**: Payment completed
- **OVERDUE**: Payment is past due date

---

## 🛠️ Common Operations

### Check Total Pending Fees
```bash
# This will show the count of pending fees
curl -s "http://127.0.0.1:5000/api/fees/load-monthly?batch_id=1&year=2025" | \
  python -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for s in data['data']['fees'] for m in s['months'].values() if m['status']=='pending'))"
```

### Mark a Fee as Paid
You'll need to update the fee status through the database or create an additional endpoint. For now, you can use Python:

```python
from app import create_app
from models import db, Fee, FeeStatus
from datetime import date

app = create_app()
with app.app_context():
    fee = Fee.query.get(2)  # February fee
    fee.status = FeeStatus.PAID
    fee.paid_date = date.today()
    fee.payment_method = 'Cash'
    db.session.commit()
    print('Fee marked as paid!')
```

### Generate Monthly Report
```bash
curl -s "http://127.0.0.1:5000/api/fees/load-monthly?batch_id=1&year=2025" | \
  python -m json.tool
```

---

## 📈 Next Steps for Financial Management

### Recommended Enhancements

1. **Mark as Paid Endpoint**
   - Create endpoint to mark fees as paid
   - Record payment method and transaction details

2. **Fee Reports**
   - Monthly collection report
   - Outstanding fees report
   - Student payment history

3. **Bulk Operations**
   - Set fees for all students in a batch
   - Apply discounts to multiple students
   - Generate fee invoices

4. **Payment Methods Integration**
   - bKash integration
   - Nagad integration
   - Bank transfer tracking

5. **Notifications**
   - SMS reminders for pending fees
   - Payment confirmation messages
   - Overdue payment alerts

6. **Dashboard Analytics**
   - Total revenue per month
   - Collection rate percentage
   - Outstanding amount summary

---

## 🔧 Troubleshooting

### Server Not Running
```bash
# Check if server is running
ps aux | grep "python.*app.py"

# Start the server
python /workspaces/madrasha/app.py
```

### Database Issues
```bash
# Recreate database with default users
python /workspaces/madrasha/create_default_users.py

# Setup test fee data
python /workspaces/madrasha/setup_test_fee_data.py
```

### Check Server Logs
```bash
tail -f /tmp/flask.log
```

---

## 📞 API Testing with Authentication

Most endpoints require authentication. To test with authentication:

```bash
# Login first
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber":"01712345678","password":"admin123"}' \
  -c cookies.txt

# Then use the session cookie
curl http://127.0.0.1:5000/api/fees/load-monthly?batch_id=1&year=2025 \
  -b cookies.txt
```

---

## 📝 Notes

- The system uses SQLite database by default (file: `smartgardenhub.db`)
- All amounts are stored as decimal values for precision
- Date formats follow ISO 8601 (YYYY-MM-DD)
- The system automatically calculates due dates (last day of month)
- Fee status is automatically managed based on due dates

---

## 🎯 Quick Start Checklist

- [x] Server is running on http://127.0.0.1:5000
- [x] Database created with default users
- [x] Test batches and fees created
- [x] Fee management API endpoints working
- [ ] Login to the system with admin credentials
- [ ] Navigate to fee management section
- [ ] Test creating/updating fees
- [ ] Generate reports

---

**System Status**: ✅ **OPERATIONAL**

Access the application at: http://127.0.0.1:5000
