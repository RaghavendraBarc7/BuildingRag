from langchain.tools import tool 

def create_search_tool(retriever):
    """Return a @tool function that searches the HR Policy document."""
    
    @tool
    def search_hr_policy(question: str) -> str:
        """Search the HR Policy document for information about leave, work from home, probation, notice period, reimbursement, code of conduct, holidays or exit process."""
        matching_chunks = retriever.invoke(question)
        return "\n\n".join(chunk.page_content for chunk in matching_chunks)
    
    return search_hr_policy