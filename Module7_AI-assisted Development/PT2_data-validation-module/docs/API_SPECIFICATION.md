# API Specification - Data Validation Module

## Base Information

- **Base URL**: `http://localhost:3000/api/v1`
- **Version**: 1.0.0
- **Protocol**: HTTP/HTTPS
- **Content-Type**: `application/json`
- **Authentication**: None (public endpoints with rate limiting)

## Rate Limiting

- **Limit**: 100 requests per minute per IP address
- **Response Header**: `X-RateLimit-Remaining`
- **Exceeded Response**: HTTP 429 with retry-after information

---

## Endpoints

### 1. POST /validate

Validates user input data (email, password, and/or phone number).

#### Request

**Method**: `POST`  
**URL**: `/api/v1/validate`  
**Headers**:
```
Content-Type: application/json
```

**Body Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | No | Email address to validate |
| password | string | No | Password to validate |
| phone | string | No | Phone number to validate (international format) |

**Note**: At least one parameter must be provided.

#### Request Examples

**Example 1: Validate all fields**
```json
POST /api/v1/validate
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "SecurePass123!",
  "phone": "+12345678901"
}
```

**Example 2: Validate only email**
```json
POST /api/v1/validate
Content-Type: application/json

{
  "email": "user@domain.com"
}
```

**Example 3: Validate password and phone**
```json
POST /api/v1/validate
Content-Type: application/json

{
  "password": "MyP@ssw0rd",
  "phone": "(123) 456-7890"
}
```

#### Response

**Success Response** (HTTP 200):
```json
{
  "valid": true,
  "errors": []
}
```

**Validation Failed Response** (HTTP 400):
```json
{
  "valid": false,
  "errors": [
    {
      "field": "email",
      "rule": "email_format",
      "message": "Invalid email format. Must be in format: user@domain.com",
      "code": "VAL_001"
    },
    {
      "field": "password",
      "rule": "password_number",
      "message": "Password must contain at least one number",
      "code": "VAL_002"
    }
  ]
}
```

**No Data Provided** (HTTP 400):
```json
{
  "valid": false,
  "errors": [
    {
      "field": "general",
      "rule": "no_data",
      "message": "No data provided for validation",
      "code": "VAL_004"
    }
  ]
}
```

**Internal Error** (HTTP 500):
```json
{
  "valid": false,
  "errors": [
    {
      "field": "general",
      "rule": "internal_error",
      "message": "Internal validation error occurred",
      "code": "SYS_001"
    }
  ]
}
```

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| valid | boolean | `true` if all validations passed, `false` otherwise |
| errors | array | Array of error objects (empty if valid=true) |

**Error Object Schema**:
| Field | Type | Description |
|-------|------|-------------|
| field | string | Field name that failed validation |
| rule | string | Rule name that was violated |
| message | string | Human-readable error message |
| code | string | Error code for programmatic handling |

---

### 2. GET /validation-rules

Retrieves all validation rules from the database.

#### Request

**Method**: `GET`  
**URL**: `/api/v1/validation-rules`  
**Headers**: None required

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| field_type | string | No | - | Filter by field type (email, password, phone) |
| active_only | boolean | No | true | Return only active rules |

#### Request Examples

**Example 1: Get all active rules**
```
GET /api/v1/validation-rules
```

**Example 2: Get email rules only**
```
GET /api/v1/validation-rules?field_type=email
```

**Example 3: Get all rules including inactive**
```
GET /api/v1/validation-rules?active_only=false
```

#### Response

**Success Response** (HTTP 200):
```json
{
  "rules": [
    {
      "id": 1,
      "rule_name": "email_format",
      "field_type": "email",
      "regex_pattern": "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$",
      "error_message": "Invalid email format. Must be in format: user@domain.com",
      "error_code": "VAL_001",
      "priority": "high",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "rule_name": "password_length",
      "field_type": "password",
      "regex_pattern": null,
      "error_message": "Password must be between 8 and 128 characters",
      "error_code": "VAL_005",
      "priority": "critical",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 2,
  "filtered": true
}
```

**Database Error** (HTTP 503):
```json
{
  "error": "Service unavailable",
  "message": "Unable to retrieve validation rules",
  "code": "SYS_002"
}
```

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| rules | array | Array of validation rule objects |
| count | number | Number of rules returned |
| filtered | boolean | Whether filters were applied |

**Rule Object Schema**:
| Field | Type | Description |
|-------|------|-------------|
| id | number | Unique rule identifier |
| rule_name | string | Unique rule name |
| field_type | string | Field type (email, password, phone, general) |
| regex_pattern | string\|null | Regular expression pattern (if applicable) |
| error_message | string | Error message to display on validation failure |
| error_code | string | Error code for programmatic handling |
| priority | string | Rule priority (critical, high, medium, low) |
| is_active | boolean | Whether rule is currently active |
| created_at | string | ISO 8601 timestamp of creation |
| updated_at | string | ISO 8601 timestamp of last update |

---

### 3. GET /validation-rules/:id

Retrieves a specific validation rule by ID.

#### Request

**Method**: `GET`  
**URL**: `/api/v1/validation-rules/:id`  
**Headers**: None required

**URL Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | number | Yes | Validation rule ID |

#### Request Example

```
GET /api/v1/validation-rules/1
```

#### Response

**Success Response** (HTTP 200):
```json
{
  "id": 1,
  "rule_name": "email_format",
  "field_type": "email",
  "regex_pattern": "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$",
  "error_message": "Invalid email format. Must be in format: user@domain.com",
  "error_code": "VAL_001",
  "priority": "high",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Not Found** (HTTP 404):
```json
{
  "error": "Not found",
  "message": "Validation rule not found"
}
```

---

### 4. GET /health

Health check endpoint for monitoring service availability.

#### Request

**Method**: `GET`  
**URL**: `/api/v1/health`  
**Headers**: None required

#### Request Example

```
GET /api/v1/health
```

#### Response

**Success Response** (HTTP 200):
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "Data Validation API",
  "version": "1.0.0"
}
```

---

## Error Codes Reference

| Code | Description | HTTP Status | Field Type |
|------|-------------|-------------|------------|
| VAL_001 | Invalid email format | 400 | email |
| VAL_002 | Invalid password format | 400 | password |
| VAL_003 | Invalid phone number format | 400 | phone |
| VAL_004 | Missing required field | 400 | general |
| VAL_005 | Field length violation | 400 | various |
| SYS_001 | Internal validation error | 500 | general |
| SYS_002 | Database connection error | 503 | general |

---

## Common Use Cases

### Use Case 1: User Registration Form
```javascript
// Frontend validation before submission
const formData = {
  email: document.getElementById('email').value,
  password: document.getElementById('password').value,
  phone: document.getElementById('phone').value
};

fetch('/api/v1/validate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(formData)
})
.then(res => res.json())
.then(data => {
  if (data.valid) {
    // Submit form
    submitRegistration(formData);
  } else {
    // Display errors
    displayErrors(data.errors);
  }
});
```

### Use Case 2: Real-time Password Strength Indicator
```javascript
// Validate password as user types
document.getElementById('password').addEventListener('input', async (e) => {
  const response = await fetch('/api/v1/validate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password: e.target.value })
  });
  
  const data = await response.json();
  updatePasswordStrength(data);
});
```

### Use Case 3: Dynamic Rule Management
```javascript
// Load validation rules for custom UI
fetch('/api/v1/validation-rules?field_type=password')
  .then(res => res.json())
  .then(data => {
    data.rules.forEach(rule => {
      displayRuleRequirement(rule);
    });
  });
```

---

## Performance Considerations

- **Response Time**: < 10ms average per validation request
- **Throughput**: Handles 1000+ requests/second
- **Caching**: Validation rules cached in memory
- **Database**: Connection pooling for optimal performance

---

## Security Considerations

1. **Input Sanitization**: All inputs sanitized before validation
2. **SQL Injection Prevention**: Parameterized queries only
3. **XSS Protection**: Error messages HTML-escaped
4. **Rate Limiting**: Prevents abuse (100 req/min per IP)
5. **HTTPS**: Recommended for production
6. **No Sensitive Data Logging**: Passwords never logged

---

## Testing Endpoints

Use these cURL commands to test the API:

```bash
# Test validation endpoint
curl -X POST http://localhost:3000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","phone":"+1234567890"}'

# Get all validation rules
curl http://localhost:3000/api/v1/validation-rules

# Get email rules only
curl http://localhost:3000/api/v1/validation-rules?field_type=email

# Health check
curl http://localhost:3000/api/v1/health
```
