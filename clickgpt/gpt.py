from openai import OpenAI

class OpenAITextRequest:
    client:OpenAI = None
    request:str = ""
    model:str = "gpt-4"

    def __init__(self, client:OpenAI, request:str, **kwargs) -> None:
        self.client = client
        self.request = request
        self.model = kwargs.get('model', self.model)
        

def create_client(api_key:str) -> OpenAI:
    client = OpenAI(api_key=api_key)
    return client

def text_request(request:OpenAITextRequest) -> str:
    if request is None: return ""

    response = request.client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.request}]
    )

    response_text = response.choices[0].message.content
    return response_text