/**
 * Utility functions for formatting data for display.
 * Following KISS principle - simple, reusable formatting functions.
 */

/**
 * Formats a date string from ISO format to Brazilian format (DD/MM/YYYY)
 * @param dateString - ISO date string (YYYY-MM-DD)
 * @returns Formatted date string (DD/MM/YYYY)
 */
export const formatDateToBR = (dateString: string): string => {
  if (!dateString) return '';

  const [year, month, day] = dateString.split('-');
  return `${day}/${month}/${year}`;
};

/**
 * Formats a date string from Brazilian format to ISO format (YYYY-MM-DD)
 * @param dateString - Brazilian date string (DD/MM/YYYY)
 * @returns ISO formatted date string (YYYY-MM-DD)
 */
export const formatDateToISO = (dateString: string): string => {
  if (!dateString) return '';

  const [day, month, year] = dateString.split('/');
  return `${year}-${month}-${day}`;
};

/**
 * Formats license type to display format with description
 * @param licenseType - License type code (A, B, C, D, E)
 * @returns Formatted license string with description
 */
export const formatLicenseType = (licenseType: string): string => {
  const licenseDescriptions: Record<string, string> = {
    A: 'A - Motorcycle',
    B: 'B - Car',
    C: 'C - Small Truck',
    D: 'D - Large Truck',
    E: 'E - Truck with Trailer',
  };

  return licenseDescriptions[licenseType] || licenseType;
};

/**
 * Formats truck type to display format
 * @param truckType - Truck type code
 * @returns Human-readable truck type
 */
export const formatTruckType = (truckType: string): string => {
  return truckType
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

/**
 * Truncates a string to a maximum length with ellipsis
 * @param text - Text to truncate
 * @param maxLength - Maximum length before truncation
 * @returns Truncated text with ellipsis if needed
 */
export const truncateText = (text: string, maxLength: number = 50): string => {
  if (!text || text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Capitalizes the first letter of each word in a string
 * @param text - Text to capitalize
 * @returns Capitalized text
 */
export const capitalizeWords = (text: string): string => {
  if (!text) return '';

  return text
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

/**
 * Formats a phone number to Brazilian format
 * @param phone - Raw phone number string
 * @returns Formatted phone number (XX) XXXXX-XXXX
 */
export const formatPhone = (phone: string): string => {
  if (!phone) return '';

  const cleaned = phone.replace(/\D/g, '');

  if (cleaned.length === 11) {
    return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 7)}-${cleaned.slice(7)}`;
  }

  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 6)}-${cleaned.slice(6)}`;
  }

  return phone;
};
