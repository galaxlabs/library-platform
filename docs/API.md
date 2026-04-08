# API Documentation

Base URL: `http://localhost:8001/api/v1`

## Authentication Endpoints

### Register
```http
POST /auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "full_name": "John Doe",
  "arabic_name": "جون دو",
  "phone": "+1234567890",
  "preferred_lang_pair": "ar-en"
}

Response 201:
{
  "user": {...},
  "tokens": {
    "access": "jwt-token",
    "refresh": "refresh-token"
  }
}
```

### Login
```http
POST /auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response 200:
{
  "user": {...},
  "tokens": {...}
}
```

### Refresh Token
```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "refresh-token"
}

Response 200:
{
  "access": "new-jwt-token"
}
```

## User Endpoints

### Get Current User Profile
```http
GET /users/me/
Authorization: Bearer {access-token}

Response 200:
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "roles": ["Student"],
  "institute": 1
}
```

### Update Profile
```http
PATCH /users/me/
Authorization: Bearer {access-token}
Content-Type: application/json

{
  "full_name": "Jane Doe",
  "phone": "+1234567899"
}

Response 200: {...updated user...}
```

## Error Responses

```json
{
  "detail": "Authentication credentials were not provided.",
  "code": "not_authenticated"
}
```

Common Status Codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limited
- `500 Server Error` - Internal error

See [Swagger UI](http://localhost:8001/api/v1/docs/) for interactive documentation.
