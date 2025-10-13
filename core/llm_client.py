# core/llm_client.py
import google.generativeai as genai

class LLMClient:
    def __init__(self, model, api_key):
        genai.configure(api_key=api_key)
        # Set up the model for automatic tool use
        self.model = genai.GenerativeModel(model)

    def chat(self, prompt: str, tools: list = None) -> str:
        """
        Sends a prompt to the Gemini API and returns the response.
        If tools are provided, it handles the tool-calling loop.
        """
        try:
            model_to_use = self.model
            if tools:
                model_to_use = genai.GenerativeModel(
                    model_name=self.model.model_name,
                    tools=tools
                )

            chat = model_to_use.start_chat()
            response = chat.send_message(prompt)

            while response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                
                # Find the corresponding tool function
                tool_func = None
                for tool in tools:
                    if tool.__name__ == function_call.name:
                        tool_func = tool
                        break
                
                if not tool_func:
                    raise ValueError(f"Tool function '{function_call.name}' not found")

                # Call the tool function with arguments from the model
                args = {key: value for key, value in function_call.args.items()}
                tool_response = tool_func(**args)

                # Send the tool's output back to the model
                response = chat.send_message(
                    [{"function_response": {
                        "name": function_call.name,
                        "response": tool_response,
                        }
                    }]
                )

            return response.text

        except Exception as e:
            print(f"[LLMClient] An unexpected error occurred: {e}")
            # Return a more structured error to the caller
            return f"Error: [LLMClient] An unexpected error occurred: {e}"
