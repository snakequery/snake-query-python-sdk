# SnakeQuery Python SDK Examples

Simple, focused examples demonstrating SnakeQuery features. **Each example contains exactly one query with structured response schemas** to demonstrate best practices.

## 🔑 Setup

Set your API key as an environment variable:
```bash
export SNAKE_QUERY_API_KEY="your-api-key-here"
```

## 📁 Examples

### 1. `data_query_demo.py` - Direct Data with Schema
Query Python lists and dictionaries directly with structured responses.

```bash
python examples/data_query_demo.py
```

**Demonstrates:**
- `client.query()` with a direct data list
- `SchemaBuilder` for consistent output structure
- Type validation on local data

### 2. `url_query_demo.py` - URL Query with Schema
Query data from REST API endpoints with structured responses.

```bash
python examples/url_query_demo.py
```

**Demonstrates:**
- `client.query()` with a URL endpoint
- Fetching from the Escuela JS products API
- Schema validation for external API data

## 🛒 Data Sources

All examples use a real, public e-commerce API:

### Escuela JS Products API
- **URL**: `https://api.escuelajs.co/api/v1/products`
- **Data**: 200+ realistic products with prices, categories, descriptions, images.
- **Free**: No authentication required.
- **Direct List**: Returns a JSON list directly (no wrapper object).
- **Reliable**: A maintained educational API.

## 💡 Key Concepts

- **Schema-First Approach**: All examples use response schemas for consistency.
- **Single Query Focus**: Each example shows exactly one query pattern.
- **Type Safety**: `SchemaBuilder` ensures validated, structured responses.
- **Real Data**: Uses an actual public API, not mock data.
- **Best Practices**: Professional patterns for production use.

## 🛠 Requirements

- Python 3.7+
- `requests` library
- A valid SnakeQuery API key
- Internet connection (for public APIs)
