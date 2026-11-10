import os
from pathlib import Path
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema

from tools import web_search, web_scrape

# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")


# ==========================================
# 2. MODEL SETUP
# ==========================================

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0, api_key=GROQ_API_KEY)


# ==========================================
# 3. SEARCH AGENT
# ==========================================


def built_search_agent():

    return create_agent(model=llm, tools=[web_search])


# ==========================================
# 4. READER AGENT
# ==========================================


def built_reader_agent():

    return create_agent(model=llm, tools=[web_scrape])


# ==========================================
# 5. WRITER CHAIN
# ==========================================

writer_response_schemas = [
    ResponseSchema(name="title", description="Title of the research report"),
    ResponseSchema(
        name="introduction", description="Introduction to the research topic"
    ),
    ResponseSchema(
        name="key_findings", description="At least three detailed research findings"
    ),
    ResponseSchema(name="conclusion", description="Conclusion of the research report"),
    ResponseSchema(name="sources", description="List of URLs used in the research"),
]

writer_parser = StructuredOutputParser.from_response_schemas(writer_response_schemas)

writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert research writer.

            Write clear, structured, detailed and insightful
            research reports.

            Use only the provided research material.
            Do not invent facts or sources.

            Follow these output instructions:

            {format_instructions}
            """,
        ),
        (
            "human",
            """
            Research Topic: {topic}

            Research Gathered:
            {research}

            Create a detailed professional research report.
            Include at least three well-explained key findings.
            """,
        ),
    ]
).partial(format_instructions=writer_parser.get_format_instructions())

writer_chain = writer_prompt | llm | writer_parser


# ==========================================
# 6. CRITIC CHAIN
# ==========================================

critic_response_schemas = [
    ResponseSchema(name="score", description="Overall research report score out of 10"),
    ResponseSchema(
        name="strengths", description="List of strengths of the research report"
    ),
    ResponseSchema(
        name="areas_to_improve", description="List of specific improvements required"
    ),
    ResponseSchema(name="verdict", description="One-line final verdict on the report"),
    ResponseSchema(
        name="approved",
        description="Whether the report meets quality standards: true or false",
    ),
]

critic_parser = StructuredOutputParser.from_response_schemas(critic_response_schemas)

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a strict and constructive research critic.

            Evaluate reports based on:
            1. Factual accuracy
            2. Research depth
            3. Source quality
            4. Structure and clarity
            5. Completeness

            Be honest and specific.

            Approve a report only if it meets quality standards.
            Use a score of 8 or higher as the approval threshold.

            Follow these output instructions:

            {format_instructions}
            """,
        ),
        (
            "human",
            """
            Review the following research report:

            {report}
            """,
        ),
    ]
).partial(format_instructions=critic_parser.get_format_instructions())

critic_chain = critic_prompt | llm | critic_parser
