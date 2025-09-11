# SnakeQuery Python SDK Documentation

The official Python SDK for SnakeQuery - Transform natural language into structured data queries with AI.

## 🚀 Quick Start

### Installation

```bash
pip install snake-query-sdk
```

### Basic Usage

```python
from snake_query_sdk import SnakeQuery, SchemaBuilder
import os

# Initialize client with your API key
client = SnakeQuery(api_key=os.environ.get('SNAKE_QUERY_API_KEY'))

# Query with structured response
result = client.query(
    query='Find products under $100',
    fetch_url='https://api.example.com/products',
    response_schema=SchemaBuilder.create()
        .array(
            SchemaBuilder.create()
            .object()
            .add_string_property('name')
            .add_number_property('price', minimum=0)
            .required(['name', 'price'])
            .build()
        )
        .build()
)

print(result['response'])      # Structured data list
print(result['usageCount'])    # Token usage info
```

## 📖 Table of Contents

- [Authentication](#authentication)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
- [Schema Building](#schema-building)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## 🔐 Authentication

Get your API key from the [SnakeQuery Dashboard](https://app.snakequery.com) and initialize the client:

```python
client = SnakeQuery(api_key='sk-1234567890abcdef...')
```

### Environment Variables (Recommended)

```bash
export SNAKE_QUERY_API_KEY="sk-1234567890abcdef..."
```

```python
import os
client = SnakeQuery(api_key=os.environ.get('SNAKE_QUERY_API_KEY'))
```

## 💡 Core Concepts

### Natural Language Queries

SnakeQuery converts natural language into structured data operations:

```python
# Instead of complex filtering logic
# expensive_products = [p for p in data if p['price'] > 500 and p['category'] == 'electronics']

# Use natural language
result = client.query(
    query='Find electronics products that cost more than $500',
    data=products
)
```

### Structured Responses

Control output format with schemas for consistent, type-safe results:

```python
schema = SchemaBuilder.create() \
    .array(
        SchemaBuilder.create()
        .object()
        .add_string_property('productName')
        .add_number_property('price', minimum=0)
        .add_string_property('category')
        .required(['productName', 'price'])
        .build()
    )
    .build()
```

## 📚 API Reference

### SnakeQuery Class

#### Constructor

```python
SnakeQuery(api_key: str)
```

#### Methods

##### `query(query: str, data: any = None, fetch_url: str = None, response_schema: dict = None, debug: bool = False) -> dict`

Main method for all query operations.

**Response:**

```python
{
    'usageCount': {
        'inputTokens': int,
        'outputTokens': int,
        'totalTokens': int
    },
    'response': any
}
```

## 🏗️ Schema Building

### SchemaBuilder Class

Create structured response schemas using a fluent API:

#### Basic Types

```python
from snake_query_sdk import SchemaBuilder

# String field
SchemaBuilder.create().string(minLength=1, maxLength=100).build()

# Number field
SchemaBuilder.create().number(minimum=0, maximum=1000).build()

# Boolean field
SchemaBuilder.create().boolean().build()
```

#### Objects

```python
user_schema = SchemaBuilder.create() \
    .object() \
    .add_string_property('name') \
    .add_number_property('age', minimum=0) \
    .add_string_property('email') \
    .required(['name', 'age']) \
    .build()
```

#### Arrays

```python
users_array_schema = SchemaBuilder.create().array(user_schema).build()

# Or inline
products_schema = SchemaBuilder.create() \
    .array(
        SchemaBuilder.create()
        .object()
        .add_string_property('title')
        .add_number_property('price', minimum=0)
        .required(['title', 'price'])
        .build()
    )
    .build()
```

## 💻 Examples

### Query Direct Data

```python
products = [
    {'name': 'iPhone', 'price': 999, 'category': 'electronics'},
    {'name': 'Shoes', 'price': 129, 'category': 'fashion'}
]

result = client.query(
    query='Find products under $500 and group by category',
    data=products,
    response_schema=SchemaBuilder.create()
        .array(
            SchemaBuilder.create()
            .object()
            .add_string_property('category')
            .add_array_property('products', item_schema={
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'price': {'type': 'number'}
                }
            })
            .required(['category', 'products'])
            .build()
        )
        .build()
)
```

## ⚠️ Error Handling

### Common Errors

```python
from snake_query_sdk.exceptions import SnakeQueryError

try:
    result = client.query(
        query='Analyze sales data',
        fetch_url='https://api.example.com/sales'
    )
except SnakeQueryError as e:
    if e.status == 401:
        print('Invalid API key')
    elif e.status == 402:
        print('Insufficient credits')
    elif e.status == 500:
        print(f'Server error: {e.message}')
    elif e.status == 504:
        print('Request timeout - try a simpler query')
    else:
        print(f'Unknown error: {e.message}')
```

## ✨ Best Practices

### 1. Always Use Schemas for Production

```python
# ❌ Don't rely on free-form responses
# result = client.query(query='Get user data', data=users)

# ✅ Use structured schemas
result = client.query(query='Get user data', data=users, response_schema=user_schema)
```

### 2. Environment Variables for API Keys

```python
# ❌ Don't hardcode API keys
# client = SnakeQuery(api_key='sk-1234567890abcdef...')

# ✅ Use environment variables
import os
client = SnakeQuery(api_key=os.environ.get('SNAKE_QUERY_API_KEY'))
```

### 3. Handle Errors Gracefully

```python
# ✅ Always wrap in try-except
try:
    result = client.query(**options)
    return result['response']
except SnakeQueryError as e:
    print(f'Query failed: {e.message}')
    return None # or default value
```

## 🔗 Additional Resources

- [SnakeQuery Dashboard](https://app.snakequery.com)
- [GitHub Repository](https://github.com/your-org/snake-query-python-sdk)
