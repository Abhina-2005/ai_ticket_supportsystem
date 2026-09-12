from django.conf import settings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field
class AIResponse(BaseModel):
    suggested_response:str=Field(description="professional and concise support response")


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0
)


prompt = ChatPromptTemplate.from_template(
    """
You are a professional customer support assistant.

Generate a professional and concise response for the customer.

TICKET TITLE:
{title}

DESCRIPTION:
{description}

CATEGORY:
{category}

PRIORITY:
{priority}

STATUS:
{status}

RULES:
1. Acknowledge the customer's issue.
2. Be polite and professional.
3. Do not invent information.
4. Do not make false promises.
5. Return only the support response.
"""
)

structured_llm=llm.with_structured_output(AIResponse)

response_chain = prompt | structured_llm


def generate_ai_response(ticket):

    result = response_chain.invoke(
        {
            "title": ticket.title,
            "description": ticket.description,
            "category": ticket.category,
            "priority": ticket.priority,
            "status": ticket.status,
        }
    )

    return result.suggested_response

class AIAnalysisOutput(BaseModel):
    summary:str
    suggested_category:str
    suggested_priority:str
    sentiment:str
    suggested_response:str

analysis_llm=llm.with_structured_output(AIAnalysisOutput)

class AIAnalysisOutput(BaseModel):
    summary: str
    suggested_category: str
    suggested_priority: str
    sentiment: str
    suggested_response: str


analysis_llm = llm.with_structured_output(AIAnalysisOutput)

analysis_prompt = ChatPromptTemplate.from_template(
    """
You are a professional customer support ticket analyzer.

Analyze the following support ticket and return accurate structured information.

TICKET TITLE:
{title}

DESCRIPTION:
{description}

CATEGORY:
{category}

PRIORITY:
{priority}

STATUS:
{status}

Rules:
1. Give a short summary of the issue.
2. Suggest the most suitable category.
3. Suggest the most suitable priority.
4. Identify the customer sentiment as positive, neutral, or negative.
5. Generate a professional and concise suggested response.
6. Do not invent information.
"""
)

analysis_chain = analysis_prompt | analysis_llm


def generate_ai_analysis(ticket):
    result = analysis_chain.invoke(
    {
        "title": ticket.title,
        "description": ticket.description,
        "category": ticket.category,
        "priority": ticket.priority,
        "status": ticket.status,
    }

    )

    return result
