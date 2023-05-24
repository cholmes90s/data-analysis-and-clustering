from src.cleaning.schema import Schema
file_schema = {
  'CustomerId':
  {
    'data_type':'integer',
    'nullable': False,
    'new_column_name': 'customer_id'
  },
  'SalesOrderNumber':
  {
    'data_type': 'integer',
    'nullable': False,
    'new_column_name': 'sales_order_number'
  },
  'SalesOrderLineNumber':
  {
    'data_type': 'integer',
    'nullable': False,
    'new_column_name': 'sales_order_line_number'
  },
  'ShipDate':
  {
    'data_type': 'datetime',
    'nullable': False,
    'new_column_name': 'ship_date',
    'datetime_format': '%d/%m/%Y'
  },
  'Qty':
  {
    'data_type': 'integer',
    'nullable': False,
    'new_column_name': 'quantity'
  },
  'Brand':
  {
    'data_type': 'string',
    'nullable': True,
    'new_column_name': 'brand'
  },
  'ProductType':
  {
    'data_type': 'string',
    'nullable': True,
    'new_column_name': 'product_type'
  },
  'ProductSupplierID':
  {
    'data_type': 'string',
    'nullable': True,
    'new_column_name': 'product_supplier_id'
  },
  'Revenue':
  {
    'data_type': 'float',
    'nullable': False,
    'new_column_name': 'revenue'
  },
  'Profit':
  {
    'data_type': 'float',
    'nullable': False,
    'new_column_name': 'profit'
  },
  'Freight cost':
  {
    'data_type': 'float',
    'nullable': False,
    'new_column_name': 'freight_cost'
  },
  'SalesTeamName':
  {
    'data_type': 'string',
    'nullable': True,
    'new_column_name': 'sales_team_name'
  }
}

schema = Schema(file_schema)