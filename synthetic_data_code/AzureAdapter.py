from openai import AzureOpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()


class AzureAdapter:
    def __init__(self, api_key: str, api_endpoint: str, api_version: str):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_endpoint,
        )

    def call_model(self, prompt: str, system_prompt: str, deployment_name: str) -> str:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
            response = self.client.chat.completions.create(
                messages=messages,
                max_tokens=4096,
                temperature=1.0,
                top_p=1.0,
                response_format={"type": "json_object"},
                model=deployment_name
            )

            return response.choices[0].message.content
        except OpenAIError as e:
            return f"An Azure error occurred: {e}"