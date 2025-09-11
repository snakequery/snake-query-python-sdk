# Schema Building Guide

Learn how to create powerful response schemas using SnakeQuery's SchemaBuilder for consistent, type-safe results.

## 🎯 Why Use Schemas?

Schemas ensure your query responses are:
- **Consistent**: Same structure every time
- **Type-safe**: Guaranteed data types
- **Validated**: Required fields are present
- **Documented**: Clear data contracts

## 🏗️ SchemaBuilder Basics

### Import SchemaBuilder

```python
from snake_query_sdk import SchemaBuilder
```

### Basic Pattern

```python
schema = SchemaBuilder.create() \
  .type()           # Define base type
  .constraints()    # Add constraints
  .build()          # Generate final schema dictionary
```

## 📊 Basic Types

### String

```python
name_schema = SchemaBuilder.create().string(minLength=1, maxLength=100).build()

# Usage in query
result = client.query(
    query='Extract user names',
    data=users,
    response_schema=SchemaBuilder.create().array(name_schema).build()
)
```

### Number

```python
price_schema = SchemaBuilder.create().number(minimum=0, maximum=10000).build()

# Integer (treated as number internally)
quantity_schema = SchemaBuilder.create().integer(minimum=1).build()
```

### Boolean

```python
available_schema = SchemaBuilder.create().boolean().build()
```

## 🏢 Object Schemas

### Basic Object

```python
user_schema = SchemaBuilder.create() \
    .object() \
    .add_string_property('name') \
    .add_number_property('age', minimum=0) \
    .add_string_property('email') \
    .required(['name', 'age']) \
    .build()
```

### Nested Objects

```python
order_schema = SchemaBuilder.create() \
    .object() \
    .add_string_property('orderId') \
    .add_object_property('customer', properties={
        'name': {'type': 'string'},
        'email': {'type': 'string'}
    }) \
    .required(['orderId', 'customer']) \
    .build()
```

## 📋 Array Schemas

### Simple Arrays

```python
# Array of strings
tags_schema = SchemaBuilder.create().array({'type': 'string'}).build()

# Array of numbers
ratings_schema = SchemaBuilder.create().array({'type': 'number', 'minimum': 1, 'maximum': 5}).build()
```

### Array of Objects

```python
products_schema = SchemaBuilder.create() \
    .array(
        SchemaBuilder.create()
        .object()
        .add_string_property('name')
        .add_number_property('price', minimum=0)
        .add_string_property('category')
        .required(['name', 'price'])
        .build()
    )
    .build()

# Usage
result = client.query(
    query='Show all products with name, price and category',
    fetch_url='https://api.store.com/products',
    response_schema=products_schema
)
```

## 🎯 Advanced Patterns

### Reusable Schema Components

```python
# Define reusable schemas
address_schema = SchemaBuilder.create() \
    .object() \
    .add_string_property('street') \
    .add_string_property('city') \
    .required(['street', 'city']) \
    .build()

person_schema = SchemaBuilder.create() \
    .object() \
    .add_string_property('name') \
    .add_string_property('email') \
    .add_property('address', address_schema) \
    .required(['name', 'email']) \
    .build()

# Use in larger schemas
employee_schema = SchemaBuilder.create() \
    .object() \
    .add_property('personalInfo', person_schema) \
    .add_string_property('employeeId') \
    .required(['personalInfo', 'employeeId']) \
    .build()
```

## 📈 Real-World Example

### Sales Analytics Dashboard

```python
sales_analytics_schema = SchemaBuilder.create() \
    .object() \
    .add_object_property('summary', properties={
        'totalRevenue': {'type': 'number', 'minimum': 0},
        'totalOrders': {'type': 'number', 'minimum': 0}
    }) \
    .add_array_property('dailyStats',
        item_schema=SchemaBuilder.create()
        .object()
        .add_string_property('date')
        .add_number_property('revenue', minimum=0)
        .required(['date', 'revenue'])
        .build()
    ) \
    .add_array_property('insights', item_schema={'type': 'string'}) \
    .required(['summary', 'dailyStats']) \
    .build()

result = client.query(
    query='Create sales dashboard with daily stats and key insights',
    fetch_url='https://api.company.com/sales',
    response_schema=sales_analytics_schema
)
```

## 🎯 Best Practices Summary

1. **Start Simple**: Begin with basic schemas and add complexity as needed.
2. **Be Specific**: Define exact field names and types you expect.
3. **Use Constraints**: Set appropriate minimum/maximum values.
4. **Mark Required Fields**: Always specify which fields are essential.
5. **Keep It Focused**: Create schemas for specific use cases.
6. **Reuse Components**: Define common patterns once.
