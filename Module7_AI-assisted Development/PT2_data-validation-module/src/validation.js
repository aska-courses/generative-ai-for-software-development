/**
 * Data Validation Module
 * Provides comprehensive validation for email, password, and phone number inputs
 * @module validation
 */

/**
 * Email validation function
 * Validates email format according to RFC 5322 (simplified)
 * @param {string} email - Email address to validate
 * @returns {{valid: boolean, errors: Array<{field: string, rule: string, message: string}>}}
 */
const validateEmail = (email) => {
  const errors = [];

  // Check if email is provided
  if (!email || email.trim() === '') {
    errors.push({
      field: 'email',
      rule: 'email_required',
      message: 'Email is required',
      code: 'VAL_004'
    });
    return { valid: false, errors };
  }

  // Convert to string and trim
  const emailStr = String(email).trim();

  // Check length constraints
  if (emailStr.length < 5 || emailStr.length > 254) {
    errors.push({
      field: 'email',
      rule: 'email_length',
      message: 'Email must be between 5 and 254 characters',
      code: 'VAL_005'
    });
  }

  // Email format validation (RFC 5322 simplified)
  const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  
  if (!emailRegex.test(emailStr)) {
    errors.push({
      field: 'email',
      rule: 'email_format',
      message: 'Invalid email format. Must be in format: user@domain.com',
      code: 'VAL_001'
    });
  }

  // Additional checks for common mistakes
  if (emailStr.includes('..') || emailStr.includes('@.') || emailStr.includes('.@')) {
    errors.push({
      field: 'email',
      rule: 'email_format',
      message: 'Invalid email format. Consecutive dots are not allowed',
      code: 'VAL_001'
    });
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Password validation function
 * Validates password strength (8+ chars, uppercase, lowercase, number, special char)
 * @param {string} password - Password to validate
 * @returns {{valid: boolean, errors: Array<{field: string, rule: string, message: string}>}}
 */
const validatePassword = (password) => {
  const errors = [];

  // Check if password is provided
  if (!password || password.trim() === '') {
    errors.push({
      field: 'password',
      rule: 'password_required',
      message: 'Password is required',
      code: 'VAL_004'
    });
    return { valid: false, errors };
  }

  const passwordStr = String(password);

  // Length validation (8-128 characters)
  if (passwordStr.length < 8 || passwordStr.length > 128) {
    errors.push({
      field: 'password',
      rule: 'password_length',
      message: 'Password must be between 8 and 128 characters',
      code: 'VAL_005'
    });
  }

  // Uppercase letter check
  if (!/[A-Z]/.test(passwordStr)) {
    errors.push({
      field: 'password',
      rule: 'password_uppercase',
      message: 'Password must contain at least one uppercase letter',
      code: 'VAL_002'
    });
  }

  // Lowercase letter check
  if (!/[a-z]/.test(passwordStr)) {
    errors.push({
      field: 'password',
      rule: 'password_lowercase',
      message: 'Password must contain at least one lowercase letter',
      code: 'VAL_002'
    });
  }

  // Number check
  if (!/[0-9]/.test(passwordStr)) {
    errors.push({
      field: 'password',
      rule: 'password_number',
      message: 'Password must contain at least one number',
      code: 'VAL_002'
    });
  }

  // Special character check
  if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(passwordStr)) {
    errors.push({
      field: 'password',
      rule: 'password_special',
      message: 'Password must contain at least one special character (!@#$%^&*...)',
      code: 'VAL_002'
    });
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Phone number validation function
 * Validates international phone format (E.164)
 * @param {string} phone - Phone number to validate
 * @returns {{valid: boolean, errors: Array<{field: string, rule: string, message: string}>}}
 */
const validatePhone = (phone) => {
  const errors = [];

  // Check if phone is provided
  if (!phone || phone.trim() === '') {
    errors.push({
      field: 'phone',
      rule: 'phone_required',
      message: 'Phone number is required',
      code: 'VAL_004'
    });
    return { valid: false, errors };
  }

  const phoneStr = String(phone).trim();

  // Remove common formatting characters for validation
  const cleanedPhone = phoneStr.replace(/[\s\-().]/g, '');

  // E.164 format: +[country code][number], 7-15 digits total
  const phoneRegex = /^\+?[1-9]\d{6,14}$/;

  if (!phoneRegex.test(cleanedPhone)) {
    errors.push({
      field: 'phone',
      rule: 'phone_format',
      message: 'Invalid phone number. Use format: +1234567890 or (123) 456-7890',
      code: 'VAL_003'
    });
  }

  // Check digit count (7-15 digits)
  const digitCount = cleanedPhone.replace(/\+/g, '').length;
  if (digitCount < 7 || digitCount > 15) {
    errors.push({
      field: 'phone',
      rule: 'phone_length',
      message: 'Phone number must contain 7-15 digits',
      code: 'VAL_005'
    });
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Validate all fields at once
 * @param {Object} data - Object containing email, password, and/or phone
 * @returns {{valid: boolean, errors: Array<{field: string, rule: string, message: string}>}}
 */
const validateAll = (data) => {
  if (!data || typeof data !== 'object') {
    return {
      valid: false,
      errors: [{
        field: 'general',
        rule: 'invalid_input',
        message: 'Invalid input data. Expected an object',
        code: 'VAL_004'
      }]
    };
  }

  const allErrors = [];

  // Validate email if provided
  if (data.email !== undefined) {
    const emailResult = validateEmail(data.email);
    allErrors.push(...emailResult.errors);
  }

  // Validate password if provided
  if (data.password !== undefined) {
    const passwordResult = validatePassword(data.password);
    allErrors.push(...passwordResult.errors);
  }

  // Validate phone if provided
  if (data.phone !== undefined) {
    const phoneResult = validatePhone(data.phone);
    allErrors.push(...phoneResult.errors);
  }

  return {
    valid: allErrors.length === 0,
    errors: allErrors
  };
};

/**
 * Sanitize input to prevent XSS attacks
 * @param {string} input - Input string to sanitize
 * @returns {string} Sanitized string
 */
const sanitizeInput = (input) => {
  if (typeof input !== 'string') {
    return input;
  }
  
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
};

// Export all validation functions
module.exports = {
  validateEmail,
  validatePassword,
  validatePhone,
  validateAll,
  sanitizeInput
};
