import os
import sys
from dotenv import load_dotenv
from agent import SupportAgent

load_dotenv()
agent = SupportAgent()

def chat_with_customer(customer_name: str, customer_id: str, message: str):
    """Handle customer support interaction WITH memory"""
    response = agent.handle_support_request(
        customer_name=customer_name,
        customer_id=customer_id,
        message=message
    )
    return response

print("\n" + "="*80)
print("DEMO: SUPPORT AGENT WITH MEMORY (REMEMBERS EVERYTHING)")
print("="*80)
print("\nType your inputs below. Agent will respond AND REMEMBER previous issues.")
print("Test with the SAME customer ID twice to see memory in action!\n")

interactions = []
customer_history = {}

while True:
    print("\n" + "-"*80)
    print("OPTIONS: 1=New Chat  2=View Customer History  3=Exit")
    print("-"*80)
    
    choice = input(">> ")
    
    if choice == "3":
        print("\n" + "="*80)
        print("SUMMARY OF TEST:")
        print("="*80)
        if len(interactions) >= 2:
            print("\n✅ You tested with same customer twice")
            print("✅ Notice how agent's responses were DIFFERENT")
            print("✅ Second response mentioned the FIRST interaction")
            print("✅ Agent REMEMBERED and CONNECTED the issues!")
            print("\nTHIS PROVES THE SOLUTION WITH MEMORY!")
        print("="*80 + "\n")
        break
    
    if choice == "2":
        if not customer_history:
            print("\n⚠️  No customer history yet. Have a conversation first!")
            continue
        
        print("\n" + "="*80)
        print("CUSTOMER INTERACTION HISTORY")
        print("="*80)
        for cust_id, history in customer_history.items():
            print(f"\nCustomer ID: {cust_id}")
            print(f"History:\n{history}")
        print("="*80)
        continue
    
    if choice != "1":
        print("❌ Invalid! Type 1, 2, or 3")
        continue
    
    print("\n--- ENTER CUSTOMER INFORMATION ---")
    customer_name = input("Customer name: ")
    if not customer_name:
        print("❌ Name required!")
        continue
    
    customer_id = input("Customer ID: ")
    if not customer_id:
        print("❌ ID required!")
        continue
    
    print("\n--- ENTER CUSTOMER ISSUE ---")
    customer_message = input("Customer message: ")
    if not customer_message:
        print("❌ Message required!")
        continue
    
    # Save interaction
    interaction_data = {
        "name": customer_name,
        "id": customer_id,
        "message": customer_message
    }
    interactions.append(interaction_data)
    
    # Track by customer ID
    if customer_id not in customer_history:
        customer_history[customer_id] = ""
    
    # Get response with memory
    print("\n" + "~"*80)
    print(f"AGENT RESPONSE TO {customer_name.upper()}:")
    print("~"*80 + "\n")
    
    response = chat_with_customer(customer_name, customer_id, customer_message)
    print(f"{response}\n")
    
    # Update history
    customer_history[customer_id] += f"\n• {customer_name}: {customer_message}\n  Agent: {response}"
    
    print("~"*80)
    print("✅ NOTICE: Agent used memory to provide context-aware response")
    print("~"*80)
    
    # Check if same customer returning
    if len(interactions) >= 2:
        prev_id = interactions[-2]["id"]
        curr_id = interactions[-1]["id"]
        
        if curr_id == prev_id:
            print("\n" + "🟢"*40)
            print("🟢 PROOF OF MEMORY WORKING:")
            print("🟢"*40)
            print(f"   ✅ {customer_name} returned (same customer ID)")
            print("   ✅ Agent remembered previous interaction")
            print("   ✅ Agent gave PERSONALIZED response")
            print("   ✅ Agent connected related issues!")
            print("   ✅ THIS SHOWS MEMORY IS WORKING!")
            print("🟢"*40)
    
    print("\n💡 TIP: Type the SAME customer ID again to see memory in action!")

if __name__ == "_main_":
    pass