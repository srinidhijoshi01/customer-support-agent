import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class SupportAgent:
    """
    AI Support Agent powered by Groq LLM
    Handles customer support requests with basic memory
    """
    
    def __init__(self):
        """Initialize the support agent"""
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "qwen/qwen3-32b"
        self.customer_history = {}
        
    def get_customer_history(self, customer_id: str) -> str:
        """Get previous interactions for a customer"""
        if customer_id in self.customer_history:
            history = self.customer_history[customer_id]
            return f"\nPrevious interactions with this customer:\n{history}"
        return "\nThis is the customer's first interaction with us."
    
    def save_interaction(self, customer_id: str, customer_name: str, message: str, response: str):
        """Save customer interaction for future reference"""
        interaction = f"- {customer_name}: {message}\n  Agent: {response}"
        
        if customer_id not in self.customer_history:
            self.customer_history[customer_id] = ""
        
        self.customer_history[customer_id] += interaction + "\n"
    
    def handle_support_request(self, customer_name: str, customer_id: str, message: str) -> str:
        """Handle customer support request WITH memory"""
        
        customer_context = self.get_customer_history(customer_id)
        
        system_prompt = """You are a helpful NovaSaaS customer support agent. 
You help customers with billing issues, subscription problems, and account management.
Be empathetic, professional, and concise. Keep responses under 100 words."""
        
        user_prompt = f"""
Customer Name: {customer_name}
Customer ID: {customer_id}

{customer_context}

Current Request: {message}

Provide a helpful support response. If this customer has had billing issues before, acknowledge it and offer extra help.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            agent_response = response.choices[0].message.content
            self.save_interaction(customer_id, customer_name, message, agent_response)
            return agent_response
            
        except Exception as e:
            return f"I apologize, but I encountered an error processing your request: {str(e)}"

    def handle_support_request_no_memory(self, customer_name: str, customer_id: str, message: str) -> str:
        """Handle customer support request WITHOUT memory"""
        
        customer_context = "\nThis is the customer's first interaction with us."
        
        system_prompt = """You are a helpful NovaSaaS customer support agent. 
You help customers with billing issues, subscription problems, and account management.
Be empathetic, professional, and concise. Keep responses under 100 words."""
        
        user_prompt = f"""
Customer Name: {customer_name}
Customer ID: {customer_id}

{customer_context}

Current Request: {message}

Provide a helpful support response. Keep it brief and generic.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            agent_response = response.choices[0].message.content
            return agent_response
            
        except Exception as e:
            return f"I apologize, but I encountered an error processing your request: {str(e)}"
