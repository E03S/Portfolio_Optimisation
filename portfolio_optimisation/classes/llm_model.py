import openai
import json
from textblob import TextBlob
class LLMModel:
    def __init__(self, model_name, system_prompt, api_key, endpoint):
        """
        Initialize the LLM Model with the necessary parameters.

        Parameters:
        model_name (str): The name of the LLM model.
        system_prompt (str): The default system prompt for the model.
        api_key (str): The API key for accessing the model.
        """
        self.model_name = model_name
        self.system_prompt = system_prompt
        openai.api_key = api_key
        openai.base_url = endpoint

    def extract_json_from_text(self, text):
        """
        Extract the JSON from the LLM model response.
        """

        try:
            start = text.find('```json') + len('```json')
            end = text.find('```', start)
            json_str = text[start:end].strip()
            return json.loads(json_str)
        except Exception as e:
            print("Error extracting JSON:", e)
            return None

    def parse_json_from_response(self, response):
        """
        Parse the JSON response from the LLM model.

        Parameters:
        response (str): The response from the LLM model.

        Returns:
        list: A list of dictionaries containing the response from the LLM model.
        """
        parsed_json = None
        parsed_json = self.extract_json_from_text(response)
        if parsed_json is not None:
            return parsed_json
        try:
            response = response.replace(" ", "").replace("\n", "").replace("```", "").replace("json", "")
            parsed_json = json.loads(response)
        except:
            with open("error.txt", "a") as f:
                f.write(response)
        return parsed_json

    def log_response(self, response):
        """
        Log the tokens from the LLM model.

        Parameters:
        response (dict): The response from the LLM model.
        """
        usage = response.usage
        token_usage_message = f"Tokens used:  {usage.prompt_tokens:,} prompt + {usage.completion_tokens:,} completion = {usage.total_tokens:,} tokens\n"
        print(token_usage_message)
        cost = self.openai_api_calculate_cost(usage)        
        with open("usage.txt", "a") as f:
            f.write(token_usage_message)
            f.write(f"Total cost for {self.model_name}: ${cost:.4f}\n")

    def tokenize_and_contatenate(self, text):
        return ' '.join(TextBlob(str(text)).words)

    def openai_api_calculate_cost(self, usage):
        pricing = {
            'gpt-3.5-turbo-1106': {
                'prompt': 0.001,
                'completion': 0.002,
            },
            'gpt-4-1106-preview': {
                'prompt': 0.01,
                'completion': 0.03,
            },
            'gpt-4': {
                'prompt': 0.03,
                'completion': 0.06,
            }
        }
        try:
            model_pricing = pricing[self.model_name]
        except KeyError:
            print(f"Model {self.model_name} not found in pricing table")
            return 0
        prompt_cost = usage.prompt_tokens * model_pricing['prompt'] / 1000
        completion_cost = usage.completion_tokens * model_pricing['completion'] / 1000
        total_cost = prompt_cost + completion_cost
        print(f"Total cost for {self.model_name}: ${total_cost:.4f}\n")

        return total_cost

    async def create_message(self, user_prompt):
        """
        Create a new message using the LLM model.

        Parameters:
        user_prompt (str): The user's prompt to be sent to the model.

        Returns:
        dict: A response from the LLM model.
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.append({"role": "user", "content": user_prompt})
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        print(response)
        try :
            self.log_response(response)
        except Exception as e:
            print(e)

        response = response.choices[0].message.content
        return response
