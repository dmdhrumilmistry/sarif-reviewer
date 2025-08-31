from openai import OpenAI
from sarif_reviewer.sarif import ContextualResult

class AIAnalyzer:
    def __init__(
        self, base_url: str = "http://localhost:11434/v1", api_key: str = "ollama"
    ):
        self.openai_client = OpenAI(base_url=base_url, api_key=api_key)

    def create_prompt(self, contextual_result: ContextualResult) -> str:
        code_snippets = "\n\n".join(contextual_result.code_snippets)
        return f"""
        Analyze the following code snippet for vulnerabilities detected by sarif and search for any
        other vulnerability if present and provide fix suggestions. Only return vulnerabilities that
        has high confidence. Limit response to few lines so that developers can take action quickly.
        For valid vulnerabilities you may provide fix code snippets that has high confidence.

        Below are sarif results:
        Rule: {contextual_result.rule_id}, Level: {contextual_result.level}
        Message: {contextual_result.message.text}
        Code Snippets:
        {code_snippets}
        """

    def analyze(self, prompt_text: str, model: str = "deepseek-r1:latest", stream: bool = False):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful security engineer that helps developers understand to verify and fix security vulnerabilities in their code and provide fix suggestions based on provided contextual snippets. If there are no vulnerabilities then strictly return only 'FALSE_POSITIVE' in response and nothing else.",
            },
            {"role": "user", "content": prompt_text},
        ]

        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )

        if stream:
            for chunk in response:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)

        return response


if __name__ == "__main__":
    analyzer = AIAnalyzer()
    code_snippet = """
@router.post("/{tenant_id}/{object_type}")
@trace_function
async def create_crm_object(
    request: Request,
    tenant_id: str,
    object_type: CRMObjectType,
    data: Dict[str, Any] = Body(),
) -> Dict[str, Any]:
    api_key = request.headers.get("api-key")
    print(api_key)
    if not api_key:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if api_key != "897123fag-908fn-7895-4452-laksdjjoi21523":
        raise HTTPException(status_code=401, detail="Invalid auth key")
    return await crm_controller.create_crm_object(object_type, data, tenant_id)    
"""
    prompt = f"Analyze the following code snippet for vulnerabilities detected by sarif and search for any other vulnerability if present and provide fix suggestions. Only return vulnerabilities that has high confidence. Limit response to few lines so that developers can take action quickly. For valid vulnerabilities you may provide fix code snippets that has high confidence.: {code_snippet}"
    response = analyzer.analyze(prompt, model="gpt-oss:20b", stream=True)
    
    print(response) # for streamed output

    # for choice in response.choices:
    #     print(choice.message.content.split("</think>")[-1])
    #     print("-" * 40)
