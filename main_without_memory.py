import os
import sys
from dotenv import load_dotenv
from agent import SupportAgent

load_dotenv()
agent = SupportAgent()

def chat_with_customer(customer_name: str, customer_id: str, message: str):
    response = agent.handle_support_request_no_memory(
        customer_name=customer_name,
        customer_id=customer_id,
        message=message
    )
    return response

print("\n" + "="*80)
print("DEMO: SUPPORT AGENT WITHOUT MEMORY (MANUAL INPUT)")
print("="*80)
print("\nType your inputs below. Agent will respond WITHOUT remembering.")

interactions = []

while True:
    print("\n" + "-"*80)
    print("OPTIONS: 1=New Chat  2=Exit")
    print("-"*80)
    
    choice = input(">> ")
    
    if choice == "2":
        print("\n" + "="*80)
        print("SUMMARY OF TEST:")
        print("="*80)
        if len(interactions) >= 2:
            print("\n✅ You tested with same customer twice")
            print("❌ Notice how agent gave generic responses both times")
            print("❌ Agent did NOT remember the first interaction")
            print("\nTHIS PROVES THE PROBLEM WITHOUT MEMORY!")
        print("="*80 + "\n")
        break
    
    if choice != "1":
        print("Invalid! Type 1 or 2")
        continue
    
    print("\n--- Enter Customer Information ---")
    customer_name = input("Customer name: ")
    if not customer_name:
        print("Name required!")
        continue
    
    customer_id = input("Customer ID: ")
    if not customer_id:
        print("ID required!")
        continue
    
    print("\n--- Enter Customer Issue ---")
    customer_message = input("Customer message: ")
    if not customer_message:
        print("Message required!")
        continue
    
    # Save interaction
    interactions.append({
        "name": customer_name,
        "id": customer_id,
        "message": customer_message
    })
    
    # Get response
    print("\n" + "~"*80)
    print(f"AGENT RESPONSE TO {customer_name.upper()}:")
    print("~"*80 + "\n")
    
    response = chat_with_customer(customer_name, customer_id, customer_message)
    print(f"{response}\n")
    
    print("~"*80)
    print("⚠️  NOTICE: Generic response - Agent did NOT remember")
    print("           anything from previous interactions!")
    print("~"*80)
    
    # Check if same customer
    if len(interactions) >= 2:
        if interactions[-1]["id"] == interactions[-2]["id"]:
            print("\n🔴 PROOF OF NO MEMORY:")
            print(f"   • {customer_name} came back")
            print("   • Agent gave GENERIC response again")
            print("   • Agent did NOT mention the previous issue")
            print("   • THIS SHOWS THE PROBLEM!")

if __name__ == "_main_":
    pass