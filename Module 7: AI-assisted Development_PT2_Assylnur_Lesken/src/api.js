/**
 * Data Validation API
 * RESTful API endpoints for data validation services
 */

const express = require('express');
const { validateAll, sanitizeInput } = require('./validation');
const router = express.Router();

// Middleware for request validation and sanitization
const sanitizeRequest = (req, res, next) => {
  if (req.body && typeof req.body === 'object') {
    Object.keys(req.body).forEach(key => {
      if (typeof req.body[key] === 'string') {
        req.body[key] = sanitizeInput(req.body[key]);
      }
    });
  }
  next();
};

// Rate limiting helper (basic implementation)
const requestCounts = new Map();
const RATE_LIMIT = 100; // requests per minute
const RATE_WINDOW = 60000; // 1 minute in ms

const rateLimiter = (req, res, next) => {
  const ip = req.ip || req.connection.remoteAddress;
  const now = Date.now();
  
  if (!requestCounts.has(ip)) {
    requestCounts.set(ip, { count: 1, resetTime: now + RATE_WINDOW });
    return next();
  }
  
  const clientData = requestCounts.get(ip);
  
  if (now > clientData.resetTime) {
    clientData.count = 1;
    clientData.resetTime = now + RATE_WINDOW;
    return next();
  }
  
  if (clientData.count >= RATE_LIMIT) {
    return res.status(429).json({
      error: 'Too many requests',
      message: 'Rate limit exceeded. Please try again later.',
      retryAfter: Math.ceil((clientData.resetTime - now) / 1000)
    });
  }
  
  clientData.count++;
  next();
};

/**
 * @route POST /validate
 * @description Validate user input data (email, password, phone)
 * @access Public (with rate limiting)
 * 
 * @param {Object} req.body - Validation data
 * @param {string} [req.body.email] - Email to validate
 * @param {string} [req.body.password] - Password to validate
 * @param {string} [req.body.phone] - Phone number to validate
 * 
 * @returns {Object} 200 - Validation result
 * @returns {boolean} valid - Whether all validations passed
 * @returns {Array} errors - Array of validation errors (empty if valid)
 * 
 * @example
 * // Request
 * POST /validate
 * Content-Type: application/json
 * {
 *   "email": "user@example.com",
 *   "password": "SecurePass123!",
 *   "phone": "+1234567890"
 * }
 * 
 * // Response (Success)
 * {
 *   "valid": true,
 *   "errors": []
 * }
 * 
 * // Response (Failure)
 * {
 *   "valid": false,
 *   "errors": [
 *     {
 *       "field": "email",
 *       "rule": "email_format",
 *       "message": "Invalid email format. Must be in format: user@domain.com",
 *       "code": "VAL_001"
 *     }
 *   ]
 * }
 */
router.post('/validate', rateLimiter, sanitizeRequest, (req, res) => {
  try {
    const { email, password, phone } = req.body;
    
    // Validate input
    const validationData = {};
    if (email !== undefined) validationData.email = email;
    if (password !== undefined) validationData.password = password;
    if (phone !== undefined) validationData.phone = phone;
    
    // Check if at least one field is provided
    if (Object.keys(validationData).length === 0) {
      return res.status(400).json({
        valid: false,
        errors: [{
          field: 'general',
          rule: 'no_data',
          message: 'No data provided for validation',
          code: 'VAL_004'
        }]
      });
    }
    
    // Perform validation
    const result = validateAll(validationData);
    
    // Return appropriate status code
    const statusCode = result.valid ? 200 : 400;
    
    res.status(statusCode).json(result);
    
  } catch (error) {
    console.error('Validation error:', error);
    res.status(500).json({
      valid: false,
      errors: [{
        field: 'general',
        rule: 'internal_error',
        message: 'Internal validation error occurred',
        code: 'SYS_001'
      }]
    });
  }
});

/**
 * @route GET /validation-rules
 * @description Retrieve all validation rules from the database
 * @access Public
 * 
 * @query {string} [field_type] - Filter by field type (email, password, phone)
 * @query {boolean} [active_only=true] - Only return active rules
 * 
 * @returns {Object} 200 - Validation rules
 * @returns {Array} rules - Array of validation rule objects
 * 
 * @example
 * // Request
 * GET /validation-rules?field_type=email&active_only=true
 * 
 * // Response
 * {
 *   "rules": [
 *     {
 *       "id": 1,
 *       "rule_name": "email_format",
 *       "field_type": "email",
 *       "regex_pattern": "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$",
 *       "error_message": "Invalid email format. Must be in format: user@domain.com",
 *       "error_code": "VAL_001",
 *       "priority": "high",
 *       "is_active": true,
 *       "created_at": "2024-01-15T10:30:00Z",
 *       "updated_at": "2024-01-15T10:30:00Z"
 *     }
 *   ],
 *   "count": 1,
 *   "filtered": true
 * }
 */
router.get('/validation-rules', async (req, res) => {
  try {
    // Note: This is a mock implementation
    // In production, replace with actual database query
    const { field_type, active_only = 'true' } = req.query;
    
    // Mock database query (replace with actual DB call)
    const mockRules = [
      {
        id: 1,
        rule_name: 'email_format',
        field_type: 'email',
        regex_pattern: '^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$',
        error_message: 'Invalid email format. Must be in format: user@domain.com',
        error_code: 'VAL_001',
        priority: 'high',
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 2,
        rule_name: 'password_length',
        field_type: 'password',
        regex_pattern: null,
        error_message: 'Password must be between 8 and 128 characters',
        error_code: 'VAL_005',
        priority: 'critical',
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 3,
        rule_name: 'phone_format',
        field_type: 'phone',
        regex_pattern: '^\\+?[1-9]\\d{6,14}$',
        error_message: 'Invalid phone number. Use format: +1234567890 or (123) 456-7890',
        error_code: 'VAL_003',
        priority: 'high',
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];
    
    // Filter rules
    let filteredRules = mockRules;
    
    if (field_type) {
      filteredRules = filteredRules.filter(rule => rule.field_type === field_type);
    }
    
    if (active_only === 'true') {
      filteredRules = filteredRules.filter(rule => rule.is_active === true);
    }
    
    res.status(200).json({
      rules: filteredRules,
      count: filteredRules.length,
      filtered: !!field_type || active_only === 'true'
    });
    
  } catch (error) {
    console.error('Database error:', error);
    res.status(503).json({
      error: 'Service unavailable',
      message: 'Unable to retrieve validation rules',
      code: 'SYS_002'
    });
  }
});

/**
 * @route GET /validation-rules/:id
 * @description Retrieve a specific validation rule by ID
 * @access Public
 * 
 * @param {number} id - Rule ID
 * 
 * @returns {Object} 200 - Validation rule
 * @returns {Object} 404 - Rule not found
 */
router.get('/validation-rules/:id', (req, res) => {
  try {
    const { id } = req.params;
    
    // Mock implementation
    const mockRule = {
      id: parseInt(id),
      rule_name: 'email_format',
      field_type: 'email',
      regex_pattern: '^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$',
      error_message: 'Invalid email format. Must be in format: user@domain.com',
      error_code: 'VAL_001',
      priority: 'high',
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    res.status(200).json(mockRule);
    
  } catch (error) {
    res.status(404).json({
      error: 'Not found',
      message: 'Validation rule not found'
    });
  }
});

/**
 * @route GET /health
 * @description Health check endpoint
 * @access Public
 */
router.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'Data Validation API',
    version: '1.0.0'
  });
});

module.exports = router;
