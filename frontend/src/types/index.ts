// Tipos para las entidades del CRM
export interface User {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  customer_count: number;
  is_admin: boolean;
}

export interface Company {
  id: string;
  name: string;
  customer_count: number;
  created_at: string;
}

export interface Customer {
  id: string;
  full_name: string;
  email: string;
  birthday_formatted: string;
  company_name: string;
  sales_rep_name: string | null;
  last_interaction_info: LastInteractionInfo | null;
  date_of_birth: string;
  created_at: string;
}

export interface CustomerDetail extends Customer {
  first_name: string;
  last_name: string;
  company: Company;
  sales_rep: User | null;
  interactions: Interaction[];
  interaction_count: number;
  updated_at: string;
}

export interface Interaction {
  id: string;
  interaction_type: InteractionType;
  notes: string;
  interaction_date: string;
  time_ago: string;
}

export interface LastInteractionInfo {
  type: InteractionType;
  time_ago: string;
  date: string;
}

// Tipos de interacción
export type InteractionType =
  | 'Call'
  | 'Email'
  | 'SMS'
  | 'Meeting'
  | 'Facebook'
  | 'LinkedIn'
  | 'WhatsApp'
  | 'Phone';

// Tipos para filtros y parámetros de búsqueda
export interface CustomerFilters {
  search?: string;
  name?: string;
  company?: string;
  sales_rep?: string;
  birthday_this_week?: boolean;
  birthday_this_month?: boolean;
  ordering?: string;
  page?: number;
}

// Tipos para respuestas de la API
export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface CustomerStats {
  total_customers: number;
  birthday_this_week: number;
  birthday_this_month: number;
}

// Tipos para formularios
export interface CustomerFormData {
  first_name: string;
  last_name: string;
  email: string;
  date_of_birth: string;
  company: string;
  sales_rep: string | null;
}

export interface InteractionFormData {
  customer: string;
  interaction_type: InteractionType;
  notes: string;
  interaction_date: string;
}
