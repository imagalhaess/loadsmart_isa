/**
 * Type definitions for the application.
 * Ensures type safety across the frontend.
 */

/**
 * License type enum matching backend
 */
export enum LicenseType {
  A = 'A',
  B = 'B',
  C = 'C',
  D = 'D',
  E = 'E',
}

/**
 * Driver entity
 */
export interface Driver {
  id: number;
  name: string;
  license_type: LicenseType;
}

/**
 * Driver creation/update request
 */
export interface DriverRequest {
  name: string;
  license_type: LicenseType;
}

/**
 * Truck entity
 */
export interface Truck {
  id: number;
  plate: string;
  minimum_license_type: LicenseType;
}

/**
 * Truck creation/update request
 */
export interface TruckRequest {
  plate: string;
  minimum_license_type: LicenseType;
}

/**
 * Assignment entity
 */
export interface Assignment {
  id: number;
  driver_id: number;
  truck_id: number;
  assignment_date: string; // ISO date string
}

/**
 * Assignment creation/update request
 */
export interface AssignmentRequest {
  driver_id: number;
  truck_id: number;
  assignment_date: string; // ISO date string
}

/**
 * API error response
 */
export interface ApiError {
  detail: string;
}
