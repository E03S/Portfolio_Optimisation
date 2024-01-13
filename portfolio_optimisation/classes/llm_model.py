import openai
import json

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

    def parse_json_from_response(self, response):
        """
        Parse the JSON response from the LLM model.

        Parameters:
        response (dict): The response from the LLM model.

        Returns:
        list: A list of dictionaries containing the response from the LLM model.
        """
        response = response.replace(" ", "").replace("\n", "").replace("```", "").replace("json", "")
        parsed_json = None
        try:
            parsed_json = json.loads(response)
        except:
            with open("error.txt", "w") as f:
                f.write(response)
        return parsed_json

    def create_message(self, user_prompt):
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
        response = response.choices[0].message.content
        return response
