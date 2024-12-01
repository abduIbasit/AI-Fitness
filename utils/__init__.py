from typing import Any


class FitnessCoach:
    def __init__(self, model: str, client: Any):
        """
        Initialize the FitnessCoach with the model and API client.

        Args:
            model (str): The language model to use.
            client (Any): The client object for interacting with the language model API.
        """
        self.model = model
        self.client = client

    def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1024,
        temperature: int = 0,
    ) -> str:
        """
        Helper method to generate a completion from the language model.

        Args:
            system_prompt (str): The system role prompt for guiding the model.
            user_prompt (str): The user input prompt to provide context.
            max_tokens (int): The maximum number of tokens for the response.

        Returns:
            str: The content of the generated response.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Error generating completion: {e}")
