from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

from loader import leads

EMAIL_TEMPLATE = "media/email_template.md"


# System prompts for Email Construction, Quality Check and Orchestrator Agents
eca_sys_msg = SystemMessage(
    content="Write an email based on the given template by filling in the"
    " template with personalized content for the lead."
)

qca_sys_msg = SystemMessage(
    content="You are a helpful assistant tasked with comparing two emails"
    " based on relevance, tone, engagement potential and selecting the best one."
    " No need for explanations."
    " Based on your analysis just return LLM_1 for first email or LLM_2 for second."
)

o10r_sys_msg = SystemMessage(
    content="You are a helpful assistant collaborating with other assistants. "
    " You are tasked with writing emails for business leads."
    " Use Email Construction Agents (ECA) and write two different emails for the same lead."
    " Wait for the response from both the ECAs."
    " Once you have the two emails use Quality Check Agent to select best one."
    " Which will tell LLM_1 or LLM_2"
    " Save all the output in a file."
    " If you get StopIteration error while getting lead data respond with no more leads in csv."
    " If there is any other error, respond with the error message and stop. "
    " If possible state possible resoution."
)

# Models
llm_EA1 = ChatOpenAI(model="gpt-3.5-turbo")
llm_EA2 = ChatOpenAI(model="gpt-3.5-turbo")
llm_QCA = ChatOpenAI(model="gpt-3.5-turbo")

llm_orchestrator = ChatOpenAI(model="gpt-3.5-turbo")

# tools functions -  here Email Construction and Quality Check Agents are also used as tools by Orchestrator


def get_email_template() -> str:
    """Get email template"""
    with open(EMAIL_TEMPLATE, "r") as f:
        return f.read().replace("\\n", "\n")


def get_lead() -> int:
    """Get next lead from lead iterator"""
    return next(leads)


def save_to_file(
    name: str,
    email: str,
    company: str,
    job_title: str,
    email_llm_1: str,
    email_llm_2: str,
    selected_email: str,
) -> None:
    """Store both generated emails along with the comparison result in a file.

    Args:
        name: str,
        email: str,
        company: str,
        job_title: str,
        email_llm_1: str,
        email_llm_2: str,
        selected_email: str

    """
    import json

    with open(f"generated/{name}.json", "w") as f:
        json.dump(
            {
                "name": name,
                "email": email,
                "company": company,
                "job_title": job_title,
                "email_llm_1": email_llm_1,
                "email_llm_2": email_llm_2,
                "selected_email": selected_email,
            },
            f,
        )


tools = [get_lead, get_email_template, save_to_file]

# agents


def email_agent_1(lead_details: str) -> str:
    """Email Construction Agent 1 used to write email based on lead data

    Args:
        lead_details: str
    """
    return llm_EA1.invoke([eca_sys_msg] + [SystemMessage(content=lead_details)])


def email_agent_2(lead_details: str) -> str:
    """Email Construction Agent 2 used to write email based on lead data

    Args:
        lead_details: str
    """
    return llm_EA2.invoke([eca_sys_msg] + [SystemMessage(content=lead_details)])


def quality_check_agent(email_1: str, email_2: str) -> str:
    """Quality check email used to compare and select the best email out of two.

    Args:
        email_1: str
        email_2: str
    """
    return llm_QCA.invoke([qca_sys_msg] + [SystemMessage(content=email_1 + email_2)])


tools += [email_agent_1, email_agent_2, quality_check_agent]


# orchestrator node
llm_with_tools = llm_orchestrator.bind_tools(tools)


# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([o10r_sys_msg] + state["messages"])]}


from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display

# Graph
builder = StateGraph(MessagesState)

# nodes: Orchestrator and tools
builder.add_node("Orchestrator", assistant)

# tools
builder.add_node("tools", ToolNode(tools))

# edges
builder.add_edge(START, "Orchestrator")

builder.add_conditional_edges("Orchestrator", tools_condition)
builder.add_edge("tools", "Orchestrator")


graph = builder.compile()
