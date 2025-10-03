import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
if WORKDIR and os.path.exists(WORKDIR):
    os.chdir(WORKDIR)
    sys.path.append(WORKDIR)

from langgraph.graph import END
from src.utils import State
from langchain_core.runnables import RunnableConfig
from typing import Literal

def should_go_to_brainstorming_idea_writer(state: State) -> Literal['human_feedback','brainstorming_idea_writer']:
    has_docs = state.get('instructor_documents', '') != ''
    print(f"🔀 Router: instructor_documents present: {has_docs}")
    if not has_docs:
        print("🔀 Router: Going to human_feedback")
        return "human_feedback"
    else:
        print("🔀 Router: Going to brainstorming_idea_writer")
        return "brainstorming_idea_writer"
    
def should_continue_with_idea_critique(state: State) -> Literal['brainstorming_idea_critique','brainstorming_narrative_writer']:
    if state.get('is_general_story_plan_approved', None) is None: 
        return "brainstorming_idea_critique"
    elif state['is_general_story_plan_approved'] == True:
        return "brainstorming_narrative_writer"
    else:
        return "brainstorming_idea_critique"

def should_continue_with_narrative_critique(state: State) -> Literal['brainstorming_narrative_critique','writer']:
    if state.get('is_detailed_story_plan_approved', None) is None: 
        return "brainstorming_narrative_critique"
    elif state['is_general_story_plan_approved'] == True:
        return "writer"
    else:
        return "brainstorming_narrative_critique"


def has_writer_ended_book(state: State, config: RunnableConfig) -> Literal["translator", "assembler", 'writer']:

    if (state['current_chapter'] == len(state['plannified_chapters_summaries']))&(state['is_chapter_approved'] == True):
        if (config.get('configurable', {}).get('language') == 'english')|(config.get('configurable', {}).get('language') is None):
            print("The translator agent is not needed in this case")
            return "assembler"
        else:
            return "translator"
    else:
        return "writer"

def has_translator_ended_book(state: State, config: RunnableConfig) -> Literal["assembler", 'translator']:

    if (state['translated_current_chapter'] == len(state['plannified_chapters_summaries'])):
        return "assembler"
    else:
        return "translator"
