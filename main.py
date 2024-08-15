from graph import process_user_input
# Пример использования
if __name__ == "__main__":
    import asyncio
    
    async def main():
        responses = await asyncio.gather(
            process_user_input("How do I transfer money?", "bot123", "user456"),
            process_user_input("I need a new card", "bot123", "user456"),
            process_user_input("Can I book a parking spot?", "bot123", "user456")
        )
        for response in responses:
            print(f"Answer: {response['answer']}")
            print(f"Tool Result: {response['tool_result']}")
            print("---")
    
    asyncio.run(main())
