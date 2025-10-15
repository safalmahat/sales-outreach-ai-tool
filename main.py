from dotenv import load_dotenv
from agents import Agent, Runner,trace,function_tool
from openai.types.responses import ResponseTextDeltaEvent
import sendgrid
import os
from sendgrid.helpers.mail import Mail,Email,To,Content 
import asyncio

from email_tools import send_email 
import certifi

load_dotenv()
os.environ['SSL_CERT_FILE']= certifi.where()

instructions1 = "You are a sales agent working for SafalAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

instructions2 = "You are a humorous, engaging sales agent working for SafalAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

instructions3 = "You are a busy sales agent working for SafalAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."


#agents
sales_agent1=Agent(
    name="Professional Sales Agent",
    instructions=instructions1,
    model="gpt-4o-mini"
)

sales_agent2=Agent(
    name="Engaging Sales Agent",
    instructions=instructions2,
    model="gpt-4o-mini"
)

sales_agent3=Agent(
    name="Busy Sales Agent",
    instructions=instructions3,
    model="gpt-4o-mini"
)
#email picker agents
sales_picker_agent_instructor=f"You pick the best cold sales email from the given options. \
    Imagine you are a customer and pick the one you are most likely to respond to. \
    Do not give an explanation; reply with the selected email only."

sales_picker_agent=Agent(
    name="Sales Picker Agent",
    instructions=sales_picker_agent_instructor,
    model="gpt-4o-mini"
)

async def main():
    result = Runner.run_streamed(sales_agent1, input="Write a cold sales email")

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

async def main_with_parallel_execution():

    message="write a cold sales email"
    with trace("Parallel cold emails"):
        results= await asyncio.gather(
        Runner.run(sales_agent1,message),
        Runner.run(sales_agent2,message),
        Runner.run(sales_agent3,message)
        )
    outputs =[result.final_output for result in results]

    for output in outputs:
        print(output +"\n\n")


async def main_with_parallel_execution_with_sales_picker_agent():
    message="write a cold sales email"
    with trace("Selection from sales people"):
        results= await asyncio.gather(
        Runner.run(sales_agent1,message),
        Runner.run(sales_agent2,message),
        Runner.run(sales_agent3,message)
        )
    outputs =[result.final_output for result in results]
    emails="Cold sales email: \n\n". join(outputs)

    best_email=await Runner.run(sales_picker_agent,emails)

    print(f"Best sales email:\n {best_email.final_output}")

async def main_with_parallel_execution_with_sales_picker_agent_using_tools():
    message="write a cold sales email"
    sales_agent_tool1=sales_agent1.as_tool(tool_name="sales_agent1", tool_description=message)
    sales_agent_tool2=sales_agent2.as_tool(tool_name="sales_agent2", tool_description=message)
    sales_agent_tool3=sales_agent3.as_tool(tool_name="sales_agent3", tool_description=message)


    tools=[sales_agent_tool1,sales_agent_tool2,sales_agent_tool3,send_email]

    # Create sales Manager Agent
    sales_manager_agent_instructor="""
        You are a Sales Manager at SafalAI. Your goal is to find the single best cold sales email using the sales_agent tools.
        Follow these steps carefully:
        1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
        2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
        3. Use the send_email tool to send the best email (and only the best email) to the user.
        Crucial Rules:
        - You must use the sales agent tools to generate the drafts — do not write them yourself.
        - You must send ONE email using the send_email tool — never more than one. 
            """
    sales_manager = Agent(name="Sales Manager", instructions=sales_manager_agent_instructor, tools=tools, model="gpt-4o-mini")

    with trace("Sales Manager"):
        result= await Runner.run(sales_manager,message)
        print(result)

# Required in Cursor too:
asyncio.run(main_with_parallel_execution_with_sales_picker_agent_using_tools())
