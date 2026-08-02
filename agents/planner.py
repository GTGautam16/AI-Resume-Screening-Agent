from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.parser import parse_resume
from agents.scorer import score_resume
from agents.interviewer import generate_interview_questions
from agents.roadmap import generate_learning_roadmap

class ResumeState(TypedDict):
    resume_text: str
    jd_text: str

    parsed_resume: dict
    analysis: dict
    interview_questions: str
    learning_roadmap: str

def parser_node(state):
    state["parsed_resume"] = parse_resume(state["resume_text"])
    return state


def scorer_node(state):
    state["analysis"] = score_resume(
        state["parsed_resume"],
        state["jd_text"]
    )
    return state


def interview_node(state):
    state["interview_questions"] = generate_interview_questions(
        state["parsed_resume"],
        state["jd_text"]
    )
    return state


def roadmap_node(state):
    state["learning_roadmap"] = generate_learning_roadmap(
        state["parsed_resume"],
        state["analysis"],
        state["jd_text"]
    )
    return state


graph = StateGraph(ResumeState)

graph.add_node("parser", parser_node)
graph.add_node("scorer", scorer_node)
graph.add_node("interviewer", interview_node)
graph.add_node("roadmap", roadmap_node)

graph.set_entry_point("parser")

graph.add_edge("parser", "scorer")
graph.add_edge("scorer", "interviewer")
graph.add_edge("interviewer", "roadmap")
graph.add_edge("roadmap", END)

resume_graph = graph.compile()


def run_resume_pipeline(resume_text, jd_text):

    return resume_graph.invoke(
        {
            "resume_text": resume_text,
            "jd_text": jd_text
        }
    )