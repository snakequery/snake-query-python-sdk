import os
from snake_query_sdk import SnakeQuery, SchemaBuilder, SnakeQueryError

def data_query_demo():
    """Demonstrates querying a local list of data with a response schema."""
    api_key = os.environ.get('SNAKE_QUERY_API_KEY')
    if not api_key:
        print("Error: SNAKE_QUERY_API_KEY environment variable not set.")
        return

    client = SnakeQuery(api_key=api_key)
    
    print('📊 Direct Data Query with Schema Demo')
    print('=======================================')
    
    try:
        products = [
            {'name': 'iPhone 14', 'price': 999, 'category': 'electronics', 'brand': 'Apple', 'stock': 50},
            {'name': 'Samsung TV', 'price': 1299, 'category': 'electronics', 'brand': 'Samsung', 'stock': 25},
            {'name': 'Nike Shoes', 'price': 129, 'category': 'fashion', 'brand': 'Nike', 'stock': 100},
            {'name': 'Adidas Jacket', 'price': 89, 'category': 'fashion', 'brand': 'Adidas', 'stock': 75},
            {'name': 'MacBook Pro', 'price': 2399, 'category': 'electronics', 'brand': 'Apple', 'stock': 15}
        ]
        
        print('\n📋 Query: Find products under $500')
        
        product_schema = (SchemaBuilder.create()
            .array(
                SchemaBuilder.create()
                .object()
                .add_string_property('productName')
                .add_number_property('price', minimum=0)
                .add_string_property('brand')
                .add_string_property('category')
                .required(['productName', 'price', 'brand'])
                .build()
            )
            .build())

        result = client.query(
            query='Find all products that cost less than $500 and show their names, prices, brands and categories',
            data=products,
            response_schema=product_schema
        )
        
        print('\n📊 Query Results:')
        print('=================')
        print(f"\n🔢 Token Usage: {result['usageCount']}")
        print(f"\n📋 Response Data: {result['response']}")
        
        if isinstance(result.get('response'), list):
            print(f"\n✨ Found {len(result['response'])} products under $500")
        
        print('\n✅ Direct data query completed successfully!')

    except SnakeQueryError as e:
        print(f'❌ Error: {e.message}')
        if e.status == 401:
            print('💡 Tip: Check your API key')

if __name__ == "__main__":
    data_query_demo()
