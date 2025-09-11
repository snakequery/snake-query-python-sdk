# Getting Started with SnakeQuery Python SDK

This guide will help you get up and running with SnakeQuery in minutes.

## 🎯 What is SnakeQuery?

SnakeQuery transforms natural language into structured data queries using AI. Instead of writing complex filtering, mapping, and aggregation logic, simply describe what you want in plain English.

**Example:**
```python
# Instead of this:
# result = sorted(
#     [item for item in data if item['price'] < 100 and item['category'] == 'electronics'],
#     key=lambda x: x['price']
# )

# Write this:
result = client.query(
    query='Find electronics under $100, show name and price, sort by price',
    data=products
)
```

## 📦 Installation

```bash
pip install snake-query-sdk
```

## 🔑 Get Your API Key

1. Visit [SnakeQuery Dashboard](https://app.snakequery.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy your key (starts with `sk-`)

## 🚀 Your First Query

Create a new file `snake_query_test.py`:

```python
from snake_query_sdk import SnakeQuery, SnakeQueryError
import os

def first_query():
    # Initialize client (best practice is to use environment variables)
    api_key = os.environ.get('SNAKE_QUERY_API_KEY', 'your-api-key-here')
    client = SnakeQuery(api_key=api_key)

    # Sample data
    products = [
        {'name': 'iPhone 14', 'price': 999, 'category': 'electronics'},
        {'name': 'Nike Shoes', 'price': 129, 'category': 'fashion'},
        {'name': 'Coffee Mug', 'price': 19, 'category': 'home'}
    ]

    try:
        result = client.query(
            query='Find products under $200',
            data=products
        )
        print('Results:', result['response'])
        print('Tokens used:', result['usageCount']['totalTokens'])
    except SnakeQueryError as e:
        print(f'Error: {e.message}')

if __name__ == "__main__":
    first_query()
```

Run it:
```bash
export SNAKE_QUERY_API_KEY="your-key"
python snake_query_test.py
```

## 🏗️ Adding Structure with Schemas

For production use, always define response schemas for consistent, type-safe results:

```python
from snake_query_sdk import SnakeQuery, SchemaBuilder, SnakeQueryError
import os

def structured_query():
    client = SnakeQuery(api_key=os.environ.get('SNAKE_QUERY_API_KEY'))

    products = [
        {'name': 'MacBook Pro', 'price': 2399, 'category': 'electronics', 'rating': 4.8},
        {'name': 'iPad Air', 'price': 599, 'category': 'electronics', 'rating': 4.5}
    ]

    # Define response structure
    product_schema = SchemaBuilder.create() \
        .array(
            SchemaBuilder.create()
            .object()
            .add_string_property('productName')
            .add_number_property('price', minimum=0)
            .add_number_property('rating', minimum=0, maximum=5)
            .required(['productName', 'price'])
            .build()
        )
        .build()

    try:
        result = client.query(
            query='Show all products with their names, prices, and ratings',
            data=products,
            response_schema=product_schema
        )
        # Result is guaranteed to match schema
        print('Structured results:', result['response'])
    except SnakeQueryError as e:
        print(f'Error: {e.message}')

if __name__ == "__main__":
    structured_query()
```

## 🌐 Querying External APIs

Query data from any REST API endpoint:

```python
from snake_query_sdk import SnakeQuery, SchemaBuilder, SnakeQueryError
import os

def query_external_api():
    client = SnakeQuery(api_key=os.environ.get('SNAKE_QUERY_API_KEY'))

    result_schema = SchemaBuilder.create() \
        .array(
            SchemaBuilder.create()
            .object()
            .add_string_property('title')
            .add_number_property('price', minimum=0)
            .add_string_property('category')
            .required(['title', 'price'])
            .build()
        )
        .build()

    try:
        result = client.query(
            query='Find products under $100, show title, price and category',
            fetch_url='https://api.escuelajs.co/api/v1/products',
            response_schema=result_schema
        )
        print('External API results:', result['response'])
        print(f"Found {len(result['response'])} products under $100")
    except SnakeQueryError as e:
        print(f'Error: {e.message}')

if __name__ == "__main__":
    query_external_api()
```

## 🎉 Next Steps

- Explore the [full API documentation](./README.md)
- Check out [advanced examples](../examples/)
- Learn about [schema building patterns](./schema-building.md)
