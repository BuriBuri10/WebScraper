import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from workflows.workflow import PersonaWorkflow

router = APIRouter()

class PersonaRequest(BaseModel):
    reddit_url: str

@router.post("/generate-persona")
async def generate_persona(data: PersonaRequest):
    """
    Endpoint to generate a persona based on a user's Reddit activity

    Extracts the username from the given Reddit profile URL, then runs the persona workflow using LangGraph

    > eg.- "reddit_url": "https://www.reddit.com/user/spez/" - replace the string with the reddit url

    Args:
        data (PersonaRequest): Contains the Reddit URL of the user

    Returns:
        dict: A dictionary with the generated persona under the key 'persona'
    """
    try:
        username = data.reddit_url.strip().split("/")[-2]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Reddit URL")

    workflow = PersonaWorkflow()
    result = await workflow.run(username=username)

    if result and result.get("response"):
        # return {"persona": result["response"]}
        persona_text = result["response"]
    
        # ✅ NEW: Create 'outputs' folder if it doesn't exist
        os.makedirs("outputs", exist_ok=True)

        # ✅ NEW: Save persona to a file
        filepath = f"outputs/{username}_persona.txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(persona_text)
        print(f"Persona saved at: {os.path.abspath(filepath)}")

        # ✅ NEW: Return download URL
        return {
            "persona": persona_text,
            "download_url": f"/api/download/{username}"
        }

    raise HTTPException(status_code=500, detail=result.get("error", "Persona generation failed"))
