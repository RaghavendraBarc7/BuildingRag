from HR_ASSISTANT.pipeline import ask, build_hr_assistant

def main():
    print("Building the HR policy assistant...")
    agent = build_hr_assistant()
    print("Assistant ready!\n")
    
    demo_questions = [
        "How many paid annual leave days do I get?", 
        "What is the notice period during probation?", 
        "Can I work from home every day?",
    ]
    
    for question in demo_questions:
        print("Question: ", question, end = "\n")
        answer = ask(agent, question)
        print("Answer: ", answer, end = "\n")
        
        
if __name__ == "__main__":
    main()
    