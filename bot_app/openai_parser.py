import openai

import dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
dotenv.load_dotenv()

openai.api_key = os.getenv("OPEN_API_KEY")


class OpenAIParser:
    """Parsing response."""

    messages = [{"role": "system", "content": open('prompt.txt.txt', 'r')}, ]

    def __init__(self, user_id):
        self.user_id = user_id

    def _get_single_response(self, message):
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[
                                                    {"role": "system",
                                                     "content": ""},
                                                    {"role": "user",
                                                     "content": message}
                                                ])
        return response["choices"][0]["message"]["content"]

    def get_response(self, userid, context_messages: list):
        self.messages.append(context_messages[-1])
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                    messages=self.messages
                                                    )
            answer = response["choices"][0]["message"]
            self.messages.append(answer)
            return answer["content"]
        except Exception as e:
            return (str(e)
                    + "\nSorry, I am not feeling well. Please try again.", 0)
