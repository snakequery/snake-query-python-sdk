import os
from snake_query_sdk import SnakeQuery, SchemaBuilder, SnakeQueryError

def url_query_demo():
    """Demonstrates querying a URL endpoint with a response schema."""
    api_key = os.environ.get('SNAKE_QUERY_API_KEY')
    if not api_key:
        print("Error: SNAKE_QUERY_API_KEY environment variable not set.")
        return

    client = SnakeQuery(api_key=api_key)
    
    print('🌐 URL Query with Schema Demo')
    print('===============================')
    
    try:
        print('\n📊 Query: Find products under $100')
        print('📡 Data Source: https://api.escuelajs.co/api/v1/products')
        
        product_schema = (SchemaBuilder.create()
            .array(
                SchemaBuilder.create()
                .object()
                .add_string_property('productTitle')
                .add_number_property('price', minimum=0)
                .add_string_property('categoryName')
                .required(['productTitle', 'price', 'categoryName'])
                .build()
            )
            .build())

        result = client.query(
            query='Show me products that cost less than $100, include title, price and category name',
            fetch_url='https://api.escuelajs.co/api/v1/products',
            response_schema=product_schema
        )
        
        print('\n📊 Query Results:')
        print('=================')
        print(f"\n🔢 Token Usage: {result['usageCount']}")
        print(f"\n📋 Response Data: {result['response']}")
        
        if isinstance(result.get('response'), list):
            print(f"\n✨ Found {len(result['response'])} products under $100")
        
        print('\n✅ Query completed successfully!')

    except SnakeQueryError as e:
        print(f'❌ Error: {e.message}')
        if e.status == 401:
            print('💡 Tip: Check your API key')
        elif e.status == 503:
            print('💡 Tip: URL might be unreachable')

if __name__ == "__main__":
    url_query_demo()
