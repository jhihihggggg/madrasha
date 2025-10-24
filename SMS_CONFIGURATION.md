# 📱 SMS Configuration - Already Configured!

## ✅ SMS is Ready to Use

Your Madrasha application has **hardcoded SMS API credentials** in the source code. You don't need to configure anything!

### Current Configuration:

- **Provider**: BulkSMSBD (http://bulksmsbd.net)
- **API Key**: `gsOKLO6XtKsANCvgPHNt`
- **Sender ID**: `8809617628909`
- **API URL**: `http://bulksmsbd.net/api/smsapi`

### Location in Code:

The SMS configuration is hardcoded in:
```
/routes/sms.py
Function: send_sms_via_api()
Lines: 116-140
```

### SMS Features Working:

✅ Attendance notifications (Present/Absent)
✅ Exam result notifications
✅ Monthly exam results
✅ Custom SMS sending
✅ SMS balance tracking
✅ SMS history and logs

### How It Works:

1. **Automatic SMS**: When teachers/ustads mark attendance and check "Send SMS", messages are sent automatically
2. **Phone Numbers**: System sends to both guardian phone and student phone
3. **Balance**: SMS count is tracked per teacher/ustad in the database
4. **History**: All SMS are logged in the `sms_log` table

### Testing SMS:

After deployment, test SMS functionality:

1. Login as teacher (01812345678 / teacher123)
2. Go to Attendance section
3. Select a batch and mark attendance
4. Check "Send SMS notifications to parents"
5. Click "Save & Send SMS"
6. SMS will be sent via BulkSMSBD API

### SMS Balance:

- Super admin can manage SMS balance for teachers
- Go to: Dashboard → Settings → Manage SMS Balance
- Add credits to teacher accounts
- Each SMS costs 1 credit

### Changing SMS Provider (Future):

If you ever need to change the SMS provider, edit:
```bash
nano /var/www/madrasha/routes/sms.py
```

Find the `send_sms_via_api()` function and update:
- `api_key`
- `sender_id`
- `api_url`

Then restart:
```bash
sudo systemctl restart madrasha
```

---

## 🎉 No Configuration Needed!

The SMS system is **production-ready** and will work immediately after deployment. No need to edit `.env` or any configuration files!
