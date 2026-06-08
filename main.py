import os 
from typing import Annotated
from fastapi import FastAPI, Body, HTTPException
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI(title="AI Agent Task Planner")

origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

ai_client = genai.Client()

class Task_Step(BaseModel):
    step_id: int = Field(gt=0, description="The sequence number")
    action: str = Field(min_length=5, max_length=200, description="The task the agent has to perform")
    tools_required: str # The tools required for the search like "web_search", etc.

class AI_Planner_Request(BaseModel):
    user_goal: str = Field(min_length=10, description="The objective of the user")
    temperature: float = Field(default=0.2, gt=0.0, le=1.0)
    planned_steps: list[Task_Step]

class Step_Report(BaseModel):
    step_id: int 
    status: str = Field(description="Completed or Skipped")
    findings: str = Field(description="This shows the findings by the LLM in each step.")

class AI_Final_Report(BaseModel):
    summary: str = Field(description="A concise summary of the overall execution.")
    detailed_findings: list[Step_Report]    
    next_recommended_actions: list[str]

@app.post("/items/structured/")
async def run_agent_planner(
    agent_request: Annotated[AI_Planner_Request, Body(embed=True)]
):
    if not agent_request.planned_steps:
        raise HTTPException(status_code=400, detail="The Agent cannot run an Empty Planner")
    
    execution_instruction = "".join(
        [f"-Step {s.step_id} [{s.tools_required}]: {s.action}\n"
         for s in agent_request.planned_steps]
    )

    prompt = f"""
You are an elite AI agent executor. 
You ultimate goal is: {agent_request.user_goal}
Use these sequential steps perfectly for the report generation: {execution_instruction}
Provide a comprehensive final report explaining these things perfectly and in a proper manner.
"""
    
    try:
        response = ai_client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt,
            config = {
                "temperature": agent_request.temperature,
                "response_mime_type": "application/json",
                "response_schema": AI_Final_Report
            }
        )

        return {
            "status": "success",
            "goal_processed": agent_request.user_goal,
            "steps_executed_count": len(agent_request.planned_steps),
            "agent_final_report": response.parsed
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini Engine Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)