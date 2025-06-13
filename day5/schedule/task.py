import streamlit as st
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import json
import re

# 🔐 Hardcoded Gemini API Key
GOOGLE_API_KEY = "AIzaSyBapLrb07ZLSqIec5af_-upeAc6yaoiH9Y"  # ⛔ Replace with your valid Gemini API key

# 🤖 LLM Setup
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

# 🛠️ Custom Tool: Task Scheduler
def schedule_tasks(task_list: str) -> str:
    prompt = f"""
You are a helpful and health-conscious daily planner assistant.

A user has the following tasks today:
{task_list}

👉 Your job:
- Schedule ONLY between 5:00 AM and 8:00 PM (no tasks outside this range).
- Include realistic breaks.
- Output STRICTLY in JSON format.
- ❌ No explanation or extra text.

✅ Example:
[
  {{
    "time": "6:00 AM – 7:00 AM",
    "task": "Exercise",
    "reason": "Boosts energy for the day"
  }},
  {{
    "time": "7:15 AM – 8:00 AM",
    "task": "Study Python",
    "reason": "Morning is best for learning new topics"
  }}
]

Your output must begin with `[` and end with `]`. Return JSON only.
"""
    return llm.invoke(prompt).content.strip()

# ⚒️ LangChain Tool Integration
scheduler_tool = Tool(
    name="Daily Scheduler",
    func=schedule_tasks,
    description="Creates a healthy day schedule from 5:00 AM to 8:00 PM with reasoning."
)

# 🤖 Agent Setup
agent = initialize_agent(
    tools=[scheduler_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# 🌟 Streamlit UI
st.set_page_config(page_title="🧠 Smart Daily Scheduler", page_icon="⏰")
st.title("🧠 Smart Daily Scheduler ⏰")
st.markdown("Type your tasks for today (comma-separated), and I’ll generate a schedule between **5:00 AM and 8:00 PM** for you with good health and productivity habits! ☀️")

# 📥 User Input
task_input = st.text_input("📝 Enter your tasks for today:", placeholder="e.g., workout, study, content writing, team meeting")

if st.button("🧩 Create My Schedule"):
    if not task_input.strip():
        st.warning("🚨 Please enter at least one task.")
    else:
        try:
            with st.spinner("Generating your personalized schedule... ⏳"):
                response = agent.run(task_input)

                # 🔍 Try to extract valid JSON from response
                json_match = re.search(r"\[\s*{.*?}\s*]", response, re.DOTALL)
                if json_match:
                    try:
                        schedule_data = json.loads(json_match.group(0))
                        df = pd.DataFrame(schedule_data)
                        st.success("✅ Here's your optimized schedule:")
                        st.table(df)
                    except Exception as e:
                        st.warning("⚠️ JSON detected but couldn’t be parsed. Showing raw output:")
                        st.text(response)
                else:
                    st.warning("⚠️ Couldn't detect JSON format. Showing raw output:")
                    st.text(response)

        except Exception as e:
            st.error(f"❌ Oops! Something went wrong: {e}")
