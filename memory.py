import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HindsightMemory:
    """
    Memory management using Hindsight Cloud API
    Stores and retrieves customer interaction history
    """
    
    def _init_(self):
        """Initialize Hindsight memory client"""
        self.api_key = os.getenv("HINDSIGHT_API_KEY")
        self.base_url = "https://api.hindsight.vectorize.io"
        
        # For now, we're using in-memory storage
        # In production, this connects to Hindsight Cloud
        self.memories = {}
    
    def store_memory(self, customer_id: str, interaction_type: str, content: str):
        """
        Store a memory about a customer interaction
        
        Args:
            customer_id: Unique customer identifier
            interaction_type: Type of interaction (billing, subscription, etc.)
            content: The interaction content to remember
        """
        if customer_id not in self.memories:
            self.memories[customer_id] = []
        
        memory_entry = {
            "type": interaction_type,
            "content": content,
            "timestamp": self._get_timestamp()
        }
        
        self.memories[customer_id].append(memory_entry)
        return f"Memory stored for {customer_id}"
    
    def retrieve_memory(self, customer_id: str, interaction_type: str = None) -> list:
        """
        Retrieve memories for a customer
        
        Args:
            customer_id: Customer identifier
            interaction_type: Optional filter by interaction type
        
        Returns:
            List of memories
        """
        if customer_id not in self.memories:
            return []
        
        memories = self.memories[customer_id]
        
        if interaction_type:
            memories = [m for m in memories if m["type"] == interaction_type]
        
        return memories
    
    def get_customer_summary(self, customer_id: str) -> str:
        """Get a summary of all customer interactions"""
        memories = self.retrieve_memory(customer_id)
        
        if not memories:
            return "No previous interactions recorded."
        
        summary = f"Customer {customer_id} has {len(memories)} recorded interactions:\n"
        
        for i, memory in enumerate(memories, 1):
            summary += f"{i}. [{memory['type']}] {memory['content'][:100]}...\n"
        
        return summary
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def clear_customer_memory(self, customer_id: str):
        """Clear all memories for a customer"""
        if customer_id in self.memories:
            del self.memories[customer_id]
            return f"Memories cleared for {customer_id}"
        return f"No memories found for {customer_id}"