/**
 * Unit Tests for Data Validation Module
 * Framework: Jest
 * Coverage: Email, Password, Phone validation + Edge cases
 */

const {
  validateEmail,
  validatePassword,
  validatePhone,
  validateAll,
  sanitizeInput
} = require('../src/validation');

describe('Email Validation', () => {
  
  test('should validate correct email format', () => {
    const result = validateEmail('john.doe@example.com');
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('should reject email without @ symbol', () => {
    const result = validateEmail('invalidemail.com');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'email',
          rule: 'email_format',
          code: 'VAL_001'
        })
      ])
    );
  });

  test('should reject email without domain extension', () => {
    const result = validateEmail('user@domain');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'email',
          rule: 'email_format'
        })
      ])
    );
  });

  test('should reject empty email', () => {
    const result = validateEmail('');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'email',
          rule: 'email_required',
          code: 'VAL_004'
        })
      ])
    );
  });

  test('should reject null email', () => {
    const result = validateEmail(null);
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          rule: 'email_required'
        })
      ])
    );
  });

  test('should reject email that is too short', () => {
    const result = validateEmail('a@b.c');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'email',
          rule: 'email_length',
          code: 'VAL_005'
        })
      ])
    );
  });

  test('should reject email with consecutive dots', () => {
    const result = validateEmail('user..name@example.com');
    expect(result.valid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
  });

  test('should accept email with numbers and special characters', () => {
    const result = validateEmail('user.name+tag123@sub-domain.example.com');
    expect(result.valid).toBe(true);
  });

  test('should accept email with hyphens and underscores', () => {
    const result = validateEmail('first_last-name@company.co.uk');
    expect(result.valid).toBe(true);
  });
});

describe('Password Validation', () => {
  
  test('should validate strong password with all requirements', () => {
    const result = validatePassword('SecurePass123!');
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('should reject password shorter than 8 characters', () => {
    const result = validatePassword('Short1!');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'password',
          rule: 'password_length',
          code: 'VAL_005'
        })
      ])
    );
  });

  test('should reject password without uppercase letter', () => {
    const result = validatePassword('lowercase123!');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'password',
          rule: 'password_uppercase',
          code: 'VAL_002'
        })
      ])
    );
  });

  test('should reject password without lowercase letter', () => {
    const result = validatePassword('UPPERCASE123!');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'password',
          rule: 'password_lowercase'
        })
      ])
    );
  });

  test('should reject password without number', () => {
    const result = validatePassword('NoNumberPass!');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'password',
          rule: 'password_number',
          code: 'VAL_002'
        })
      ])
    );
  });

  test('should reject password without special character', () => {
    const result = validatePassword('NoSpecialChar123');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'password',
          rule: 'password_special',
          code: 'VAL_002'
        })
      ])
    );
  });

  test('should reject empty password', () => {
    const result = validatePassword('');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'password',
          rule: 'password_required',
          code: 'VAL_004'
        })
      ])
    );
  });

  test('should reject null password', () => {
    const result = validatePassword(null);
    expect(result.valid).toBe(false);
    expect(result.errors[0].rule).toBe('password_required');
  });

  test('should accept password with multiple special characters', () => {
    const result = validatePassword('P@ssw0rd!#$');
    expect(result.valid).toBe(true);
  });

  test('should accept exactly 8 character password with all requirements', () => {
    const result = validatePassword('Pass123!');
    expect(result.valid).toBe(true);
  });

  test('should reject password longer than 128 characters', () => {
    const longPassword = 'A1!' + 'a'.repeat(130);
    const result = validatePassword(longPassword);
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          rule: 'password_length'
        })
      ])
    );
  });
});

describe('Phone Number Validation', () => {
  
  test('should validate international phone with + prefix', () => {
    const result = validatePhone('+12345678901');
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('should validate phone number with formatting', () => {
    const result = validatePhone('(123) 456-7890');
    expect(result.valid).toBe(true);
  });

  test('should validate phone with spaces and hyphens', () => {
    const result = validatePhone('+1 234-567-8901');
    expect(result.valid).toBe(true);
  });

  test('should reject phone number that is too short', () => {
    const result = validatePhone('+12345');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'phone',
          rule: 'phone_length',
          code: 'VAL_005'
        })
      ])
    );
  });

  test('should reject phone number that is too long', () => {
    const result = validatePhone('+1234567890123456');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          rule: 'phone_length'
        })
      ])
    );
  });

  test('should reject empty phone number', () => {
    const result = validatePhone('');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          field: 'phone',
          rule: 'phone_required',
          code: 'VAL_004'
        })
      ])
    );
  });

  test('should reject null phone number', () => {
    const result = validatePhone(null);
    expect(result.valid).toBe(false);
    expect(result.errors[0].rule).toBe('phone_required');
  });

  test('should reject phone starting with 0', () => {
    const result = validatePhone('+0123456789');
    expect(result.valid).toBe(false);
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          rule: 'phone_format',
          code: 'VAL_003'
        })
      ])
    );
  });

  test('should accept phone without + prefix if valid format', () => {
    const result = validatePhone('12345678901');
    expect(result.valid).toBe(true);
  });

  test('should reject phone with letters', () => {
    const result = validatePhone('+1234ABC7890');
    expect(result.valid).toBe(false);
  });
});

describe('Validate All Function', () => {
  
  test('should validate all fields when all are correct', () => {
    const data = {
      email: 'user@example.com',
      password: 'SecurePass123!',
      phone: '+12345678901'
    };
    const result = validateAll(data);
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('should collect errors from multiple fields', () => {
    const data = {
      email: 'invalid-email',
      password: 'weak',
      phone: '123'
    };
    const result = validateAll(data);
    expect(result.valid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(3);
  });

  test('should validate partial data (only email)', () => {
    const data = {
      email: 'user@example.com'
    };
    const result = validateAll(data);
    expect(result.valid).toBe(true);
  });

  test('should handle empty object', () => {
    const result = validateAll({});
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('should reject null input', () => {
    const result = validateAll(null);
    expect(result.valid).toBe(false);
    expect(result.errors[0].code).toBe('VAL_004');
  });

  test('should reject non-object input', () => {
    const result = validateAll('not an object');
    expect(result.valid).toBe(false);
  });
});

describe('Input Sanitization', () => {
  
  test('should sanitize HTML tags', () => {
    const result = sanitizeInput('<script>alert("XSS")</script>');
    expect(result).toBe('&lt;script&gt;alert(&quot;XSS&quot;)&lt;&#x2F;script&gt;');
  });

  test('should sanitize special characters', () => {
    const result = sanitizeInput('Test & <tag> "quote" \'single\'');
    expect(result).toContain('&amp;');
    expect(result).toContain('&lt;');
    expect(result).toContain('&gt;');
    expect(result).toContain('&quot;');
  });

  test('should return non-string input unchanged', () => {
    const result = sanitizeInput(12345);
    expect(result).toBe(12345);
  });

  test('should handle empty string', () => {
    const result = sanitizeInput('');
    expect(result).toBe('');
  });
});

describe('Edge Cases and Security', () => {
  
  test('should handle undefined values gracefully', () => {
    const result = validateEmail(undefined);
    expect(result.valid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
  });

  test('should handle very long email addresses', () => {
    const longEmail = 'a'.repeat(250) + '@example.com';
    const result = validateEmail(longEmail);
    expect(result.valid).toBe(false);
  });

  test('should handle special characters in password correctly', () => {
    const specialChars = '!@#$%^&*()_+-=[]{}|;:,.<>?';
    const password = 'Pass123' + specialChars;
    const result = validatePassword(password);
    expect(result.valid).toBe(true);
  });

  test('should trim whitespace from email', () => {
    const result = validateEmail('  user@example.com  ');
    expect(result.valid).toBe(true);
  });

  test('should handle unicode characters in email', () => {
    const result = validateEmail('user@例え.jp');
    // This should fail as our regex is ASCII-only
    expect(result.valid).toBe(false);
  });

  test('should validate all error objects have required properties', () => {
    const result = validateEmail('invalid');
    result.errors.forEach(error => {
      expect(error).toHaveProperty('field');
      expect(error).toHaveProperty('rule');
      expect(error).toHaveProperty('message');
      expect(error).toHaveProperty('code');
    });
  });
});
