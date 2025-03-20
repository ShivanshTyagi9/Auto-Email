from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash", temperature=0.7, api_key=GOOGLE_API_KEY)

def load_past_emails(file_path="docs.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def generate_email_reply(email_body):
    past_emails = load_past_emails()  # Fetch stored emails

    prompt_template = PromptTemplate(
        input_variables=["past_emails", "email_body"],
        template="""
        You are an AI assistant that generates email replies in the style of the client.
        Below are past emails written by the client:

        {past_emails}

        Based on their style, generate a response to the following email:

        Email: {email_body}
        Response:
        """
    )

    prompt = prompt_template.format(past_emails=past_emails, email_body=email_body)
    response = llm.predict(prompt)

    return response.strip()