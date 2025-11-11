/**
 * Utility functions for validation.
 * Following Single Responsibility Principle - each validator has one specific purpose.
 */

/**
 * Validates if a date string is in valid format (YYYY-MM-DD)
 * @param dateString - Date string to validate
 * @returns True if valid, false otherwise
 */
export const isValidDate = (dateString: string): boolean => {
  if (!dateString) return false;

  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!regex.test(dateString)) return false;

  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date.getTime());
};

/**
 * Validates if end date is after start date
 * @param startDate - Start date string (YYYY-MM-DD)
 * @param endDate - End date string (YYYY-MM-DD)
 * @returns True if end date is after start date
 */
export const isEndDateAfterStartDate = (startDate: string, endDate: string): boolean => {
  if (!isValidDate(startDate) || !isValidDate(endDate)) return false;

  const start = new Date(startDate);
  const end = new Date(endDate);

  return end >= start;
};

/**
 * Validates if a string is not empty (after trimming)
 * @param value - String to validate
 * @returns True if not empty, false otherwise
 */
export const isNotEmpty = (value: string): boolean => {
  return value?.trim().length > 0;
};

/**
 * Validates if a value is a positive number
 * @param value - Value to validate
 * @returns True if positive number, false otherwise
 */
export const isPositiveNumber = (value: number | string): boolean => {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  return !isNaN(num) && num > 0;
};

/**
 * Validates license type code
 * @param licenseType - License type to validate
 * @returns True if valid license type (A, B, C, D, E)
 */
export const isValidLicenseType = (licenseType: string): boolean => {
  return ['A', 'B', 'C', 'D', 'E'].includes(licenseType?.toUpperCase());
};

/**
 * Validates if a phone number has valid format
 * @param phone - Phone number to validate
 * @returns True if valid Brazilian phone format
 */
export const isValidPhone = (phone: string): boolean => {
  if (!phone) return false;

  const cleaned = phone.replace(/\D/g, '');
  return cleaned.length === 10 || cleaned.length === 11;
};

/**
 * Validates if a string has minimum length
 * @param value - String to validate
 * @param minLength - Minimum required length
 * @returns True if meets minimum length requirement
 */
export const hasMinLength = (value: string, minLength: number): boolean => {
  return value?.trim().length >= minLength;
};

/**
 * Validates if a string has maximum length
 * @param value - String to validate
 * @param maxLength - Maximum allowed length
 * @returns True if within maximum length limit
 */
export const hasMaxLength = (value: string, maxLength: number): boolean => {
  return value?.trim().length <= maxLength;
};
