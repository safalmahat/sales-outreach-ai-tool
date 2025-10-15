from dotenv import load_dotenv
from agents import Agent, Runner,trace,function_tool
from openai.types.responses import ResponseTextDeltaEvent
import sendgrid
import os
from sendgrid.helpers.mail import Mail,Email,To,Content 
import asyncio

load_dotenv()

instructions1 = "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

instructions2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

instructions3 = "You are a busy sales agent working for ComplAI, \
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

# Required in Cursor too:
asyncio.run(main_with_parallel_execution_with_sales_picker_agent())
