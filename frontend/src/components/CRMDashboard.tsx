import React, { useState, useEffect } from 'react';
import { Search, Filter, Calendar, Building, User, Phone, Mail, MessageSquare } from 'lucide-react';
import { Customer, CustomerFilters, CustomerStats } from '../types';
import { customerService } from '../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';

const CRMDashboard: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<CustomerStats | null>(null);
  const [filters, setFilters] = useState<CustomerFilters>({
    search: '',
    ordering: 'first_name',
    page: 1
  });
  const [totalCount, setTotalCount] = useState(0);

  // Cargar datos iniciales
  useEffect(() => {
    loadCustomers();
    loadStats();
  }, [filters]);

  const loadCustomers = async () => {
    try {
      setLoading(true);
      const response = await customerService.getCustomers(filters);
      setCustomers(response.results);
      setTotalCount(response.count);
    } catch (error) {
      console.error('Error loading customers:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await customerService.getCustomerStats();
      setStats(statsData);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters(prev => ({
      ...prev,
      search: e.target.value,
      page: 1
    }));
  };

  const handleFilterChange = (key: keyof CustomerFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
      page: 1
    }));
  };

  const handleSort = (field: string) => {
    const currentOrder = filters.ordering;
    const newOrder = currentOrder === field ? `-${field}` : field;
    setFilters(prev => ({
      ...prev,
      ordering: newOrder
    }));
  };

  const getInteractionIcon = (type: string) => {
    switch (type) {
      case 'Call':
      case 'Phone':
        return <Phone className="w-4 h-4" />;
      case 'Email':
        return <Mail className="w-4 h-4" />;
      case 'SMS':
      case 'WhatsApp':
        return <MessageSquare className="w-4 h-4" />;
      default:
        return <MessageSquare className="w-4 h-4" />;
    }
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">CRM Dashboard</h1>
        <div className="text-sm text-muted-foreground">
          Total de clientes: {totalCount.toLocaleString()}
        </div>
      </div>

      {/* Estadísticas */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Clientes</CardTitle>
              <User className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_customers.toLocaleString()}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Cumpleaños esta semana</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.birthday_this_week}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Cumpleaños este mes</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.birthday_this_month}</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filtros */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="w-5 h-5" />
            Filtros y Búsqueda
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Búsqueda general */}
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar clientes..."
                value={filters.search || ''}
                onChange={handleSearchChange}
                className="pl-10"
              />
            </div>

            {/* Filtros rápidos */}
            <Button
              variant={filters.birthday_this_week ? "default" : "outline"}
              onClick={() => handleFilterChange('birthday_this_week', !filters.birthday_this_week)}
            >
              Cumpleaños esta semana
            </Button>

            <Button
              variant={filters.birthday_this_month ? "default" : "outline"}
              onClick={() => handleFilterChange('birthday_this_month', !filters.birthday_this_month)}
            >
              Cumpleaños este mes
            </Button>

            <Button
              variant="outline"
              onClick={() => setFilters({ search: '', ordering: 'first_name', page: 1 })}
            >
              Limpiar filtros
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Tabla de clientes */}
      <Card>
        <CardHeader>
          <CardTitle>Lista de Clientes</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex justify-center items-center p-8">
              <div className="text-muted-foreground">Cargando clientes...</div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th
                      className="text-left p-4 cursor-pointer hover:bg-muted/50"
                      onClick={() => handleSort('first_name')}
                    >
                      Nombre {filters.ordering?.includes('first_name') && (filters.ordering.startsWith('-') ? '↓' : '↑')}
                    </th>
                    <th
                      className="text-left p-4 cursor-pointer hover:bg-muted/50"
                      onClick={() => handleSort('company__name')}
                    >
                      Compañía {filters.ordering?.includes('company') && (filters.ordering.startsWith('-') ? '↓' : '↑')}
                    </th>
                    <th
                      className="text-left p-4 cursor-pointer hover:bg-muted/50"
                      onClick={() => handleSort('date_of_birth')}
                    >
                      Cumpleaños {filters.ordering?.includes('date_of_birth') && (filters.ordering.startsWith('-') ? '↓' : '↑')}
                    </th>
                    <th className="text-left p-4">Última Interacción</th>
                    <th className="text-left p-4">Representante</th>
                  </tr>
                </thead>
                <tbody>
                  {customers.map((customer) => (
                    <tr key={customer.id} className="border-b hover:bg-muted/50">
                      <td className="p-4">
                        <div>
                          <div className="font-medium">{customer.full_name}</div>
                          <div className="text-sm text-muted-foreground">{customer.email}</div>
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <Building className="w-4 h-4 text-muted-foreground" />
                          {customer.company_name}
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4 text-muted-foreground" />
                          {customer.birthday_formatted}
                        </div>
                      </td>
                      <td className="p-4">
                        {customer.last_interaction_info ? (
                          <div className="flex items-center gap-2">
                            {getInteractionIcon(customer.last_interaction_info.type)}
                            <span className="text-sm">
                              {customer.last_interaction_info.time_ago} ({customer.last_interaction_info.type})
                            </span>
                          </div>
                        ) : (
                          <span className="text-sm text-muted-foreground">Sin interacciones</span>
                        )}
                      </td>
                      <td className="p-4">
                        {customer.sales_rep_name ? (
                          <div className="flex items-center gap-2">
                            <User className="w-4 h-4 text-muted-foreground" />
                            {customer.sales_rep_name}
                          </div>
                        ) : (
                          <span className="text-sm text-muted-foreground">Sin asignar</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {customers.length === 0 && (
                <div className="text-center p-8 text-muted-foreground">
                  No se encontraron clientes con los filtros actuales
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CRMDashboard;
