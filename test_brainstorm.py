#!/usr/bin/env python3

from src.nodes import making_general_story_brainstorming
from src.utils import State, DocumentationReady
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

# Create test state with instructor documents
state = {
    'instructor_documents': DocumentationReady(
        reasoning_step='Test reasoning',
        reflection_step='Test reflection',
        topic='gay twins telepathy paranormal romance',
        target_audience='General adult readers',
        genre='Paranormal romance',
        writing_style='Engaging narrative',
        additional_requirements='Focus on romance and paranormal elements'
    ),
    'is_general_story_plan_approved': None
}

config = RunnableConfig(configurable={
    'brainstormer_idea_model': 'openrouter'
})

print('Testing brainstorming idea agent...')
try:
    result = making_general_story_brainstorming(state, config)
    print('Brainstorming completed successfully!')
    print('Result keys:', list(result.keys()))
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()


