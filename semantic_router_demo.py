"""
Semantic Router Demo using RedisVL

This example demonstrates how to use RedisVL's SemanticRouter to intelligently
route user queries to appropriate handlers based on semantic similarity.

Based on: https://redis.io/docs/latest/develop/ai/redisvl/api/router/
"""

from __future__ import annotations
from typing import Optional, List
from redisvl.extensions.router import SemanticRouter, Route, RoutingConfig
from redisvl.utils.vectorize import HFTextVectorizer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_sample_router():
    """
    Create a semantic router with multiple routes for different topics.
    """
    
    # Define routes with reference phrases for each topic
    routes = [
        Route(
            name="technology",
            references=[
                "What's the latest in AI?",
                "Tell me about machine learning",
                "How does cloud computing work?",
                "Explain quantum computers",
                "What are the newest programming languages?",
                "How do neural networks function?",
                "What is blockchain technology?"
            ],
            metadata={"category": "tech", "handler": "tech_handler"},
            distance_threshold=0.4
        ),
        Route(
            name="sports",
            references=[
                "Who won the game last night?",
                "What's the latest football score?",
                "Tell me about the Olympics",
                "How is my favorite team doing?",
                "What are the basketball rankings?",
                "Who holds the world record?",
                "When is the next match?"
            ],
            metadata={"category": "sports", "handler": "sports_handler"},
            distance_threshold=0.4
        ),
        Route(
            name="cooking",
            references=[
                "How do I make pasta?",
                "What's a good recipe for chicken?",
                "How to bake a cake?",
                "What ingredients do I need for pizza?",
                "How long should I cook steak?",
                "What's a healthy breakfast option?",
                "How to make vegetarian dishes?"
            ],
            metadata={"category": "cooking", "handler": "cooking_handler"},
            distance_threshold=0.4
        ),
        Route(
            name="travel",
            references=[
                "What are good places to visit in Europe?",
                "How do I plan a vacation?",
                "What's the best time to visit Japan?",
                "Where should I stay in Paris?",
                "What documents do I need for travel?",
                "How to book cheap flights?",
                "What are popular tourist attractions?"
            ],
            metadata={"category": "travel", "handler": "travel_handler"},
            distance_threshold=0.4
        ),
        Route(
            name="general",
            references=[
                "Hello",
                "How are you?",
                "What can you help me with?",
                "Tell me something interesting",
                "What's the weather like?",
                "I need help",
                "Thank you"
            ],
            metadata={"category": "general", "handler": "general_handler"},
            distance_threshold=0.5
        )
    ]
    
    # Configure routing behavior
    routing_config = RoutingConfig(
        max_k=3,  # Return top 3 matches
        aggregation_method="avg"  # Use average distance aggregation
    )
    print("Routing config object created")
   
    # Create the semantic router
    router = SemanticRouter(
        name="topic_router",
        routes=routes,
        routing_config=routing_config,
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6380"),
        overwrite=True  # Overwrite existing index if it exists
    )
    print("Router object created")
    return router


def route_query(router, query):
    """
    Route a query and display the results.
    
    Args:
        router: SemanticRouter instance
        query: User query string
    """
    print(f"\n{'='*60}")
    print(f"Query: '{query}'")
    print(f"{'='*60}")
    
    # Get route matches
    matches = router(query)
    
    # Ensure matches is a list
    if not isinstance(matches, list):
        matches = [matches] if matches else []
    
    if matches:
        print(f"\nFound {len(matches)} matching route(s):")
        for i, match in enumerate(matches, 1):
            if match.name is None:
                print(f"\n  {i}. No matching route found (distance too high)")
                continue
            print(f"\n  {i}. Route: '{match.name}'")
            print(f"     Distance: {match.distance:.4f}")
            
            # Get the route details
            route = router.get(match.name)
            if route:
                print(f"     Category: {route.metadata.get('category', 'N/A')}")
                print(f"     Handler: {route.metadata.get('handler', 'N/A')}")
                print(f"     Threshold: {route.distance_threshold}")
    else:
        print("\n  ❌ No matching routes found!")
    
    return matches


def main():
    """
    Main function to demonstrate semantic routing.
    """
    print("\n" + "="*60)
    print("  Semantic Router Demo with RedisVL")
    print("="*60)
    
    try:
        # Create the router
        print("\n📦 Creating semantic router with 5 routes...")
        router = create_sample_router()
        print("✅ Router created successfully!")
        
        # Display router information
        print(f"\nRouter Name: {router.name}")
        print(f"Number of Routes: {len(router.routes)}")
        print(f"Available Routes: {', '.join(router.route_names)}")
        print(f"Max K: {router.routing_config.max_k}")
        print(f"Aggregation Method: {router.routing_config.aggregation_method}")
        
        # Test queries
        test_queries = [
            "What's new in artificial intelligence?",
            "Who won the championship?",
            "How do I make spaghetti carbonara?",
            "Where should I travel for summer vacation?",
            "Hello, what can you do?",
            "Tell me about deep learning algorithms",
            "What are the best hiking trails?",
            "How to prepare a vegan meal?"
        ]
        
        print("\n" + "="*60)
        print("  Testing Queries")
        print("="*60)
        
        for query in test_queries:
            matches = route_query(router, query)
        
        # Example: Adding more references to a route
        print("\n" + "="*60)
        print("  Adding New References")
        print("="*60)
        
        new_refs = router.add_route_references(
            route_name="technology",
            references=[
                "What is artificial general intelligence?",
                "Explain reinforcement learning"
            ]
        )
        print(f"\n✅ Added {len(new_refs)} new references to 'technology' route")
        
        # Example: Updating route thresholds
        print("\n" + "="*60)
        print("  Updating Route Thresholds")
        print("="*60)
        
        router.update_route_thresholds({
            "technology": 0.35,
            "sports": 0.45
        })
        print("\n✅ Updated thresholds for technology and sports routes")
        
        # Save router configuration to YAML
        yaml_path = "router_config.yaml"
        router.to_yaml(yaml_path, overwrite=True)
        print(f"\n💾 Router configuration saved to '{yaml_path}'")
        
        # Example: Get route details
        print("\n" + "="*60)
        print("  Route Details")
        print("="*60)
        
        tech_route = router.get("technology")
        if tech_route:
            print(f"\nRoute: {tech_route.name}")
            print(f"Number of references: {len(tech_route.references)}")
            print(f"Distance threshold: {tech_route.distance_threshold}")
            print(f"Metadata: {tech_route.metadata}")
        
        print("\n" + "="*60)
        print("  Demo Complete! ✅")
        print("="*60)
        print("\nNote: Run router.delete() or router.clear() when done to clean up.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Redis is running")
        print("  2. redisvl is installed: pip install redisvl")
        print("  3. REDIS_URL is configured in .env (optional)")


if __name__ == "__main__":
    main()

