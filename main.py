#!/usr/bin/env python3
"""
Book Builder AI - Main Entry Point

This application creates complete books using AI agents.
You can run it in GUI mode (recommended) or CLI mode.

Usage:
    python main.py gui    # Launch the GUI version
    python main.py cli    # Launch the CLI version (original)
"""

import sys
import argparse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_gui():
    """Launch the GUI version of the application"""
    print("🚀 Starting Book Builder AI GUI...")
    print("📚 A complete book creation interface with OpenRouter support!")

    try:
        from src.gui import main
        main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print("📦 Please install required dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)

def run_cli():
    """Launch the original CLI version"""
    print("📝 Starting Book Builder AI CLI...")
    print("Note: For a better experience, use the GUI version: python main.py gui")

    try:
        # Import and run the original CLI application
        from src.agent import app
        from src.utils import GraphConfig, State
        from langchain_core.messages import HumanMessage

        print("\n" + "="*60)
        print("📚 BOOK BUILDER AI - CLI MODE")
        print("="*60)

        # Get user input for book idea
        print("\n📝 Please describe your book idea:")
        print("(e.g., 'Write a science fiction thriller about a detective who discovers a conspiracy...')")
        book_idea = input("\nYour book idea: ").strip()

        if not book_idea:
            print("❌ Please provide a book idea!")
            sys.exit(1)

        print("\n⚙️  Configuring book parameters...")

        # Configure book parameters
        config: GraphConfig = {
            'configurable': {
                'language': 'english',
                'critiques_in_loop': False,
                'instructor_model': 'openai',
                'brainstormer_idea_model': 'openai',
                'brainstormer_critique_model': 'openai',
                'writer_model': 'openai',
                'writing_reviewer_model': 'openai',
                'translator_model': 'openai',
                'n_chapters': 8,
                'min_paragraph_per_chapter': 5,
                'min_sentences_in_each_paragraph_per_chapter': 5
            }
        }

        print(f"📖 Book will have {config['configurable']['n_chapters']} chapters")
        print(f"🌐 Language: {config['configurable']['language']}")
        print("🤖 Using OpenAI models (set OPENAI_API_KEY in .env to use other models)")

        # Initialize state
        state: State = {
            'content': [],
            'translated_content': [],
            'translated_chapter_names': [],
            'content_of_approved_chapters': [],
            'chapter_names_of_approved_chapters': [],
            'chapter_names': [],
            'writer_memory': [],
            'translator_memory': [],
            'user_instructor_messages': [HumanMessage(content=book_idea)],
            'plannified_messages': [],
            'critique_brainstorming_messages': [],
            'is_general_story_plan_approved': False,
            'is_detailed_story_plan_approved': False,
            'instructor_model': '',
            'brainstorming_writer_model': '',
            'brainstorming_critique_model': '',
            'writer_model': '',
            'reviewer_model': '',
            'translator_model': '',
            'translated_book_prologue': '',
            'translated_book_name': '',
            'current_chapter': 0,
            'translated_current_chapter': 0,
            'instructor_documents': None,
            'book_prologue': '',
            'book_title': '',
            'plannified_context_setting': '',
            'plannified_inciting_incident': '',
            'plannified_themes_conflicts_intro': '',
            'plannified_transition_to_development': '',
            'plannified_rising_action': '',
            'plannified_subplots': '',
            'plannified_midpoint': '',
            'plannified_climax_build_up': '',
            'plannified_climax': '',
            'plannified_falling_action': '',
            'plannified_resolution': '',
            'plannified_epilogue': '',
            'plannified_chapters_summaries': [],
            'plannified_chapters_messages': [],
            'characters': '',
            'writing_style': '',
            'story_overview': '',
            'writing_reviewer_memory': [],
            'is_chapter_approved': False,
            'english_version_book': '',
            'translated_version_book': '',
            'critique_brainstorming_narrative_messages': []
        }

        print("\n🚀 Starting book creation process...")
        print("This may take several minutes depending on your book complexity.\n")

        # Run the book creation process
        chapter_count = 0
        for event in app.stream(state, config):
            for node_name, node_state in event.items():
                if node_name == "instructor":
                    print("👨‍🏫 Instructor Agent: Gathering and refining requirements...")
                elif node_name == "brainstorming_idea_writer":
                    print("💡 Brainstorming Agent: Creating story outline...")
                elif node_name == "brainstorming_idea_critique":
                    print("🔍 Brainstorming Critique: Reviewing story outline...")
                elif node_name == "brainstorming_narrative_writer":
                    print("📝 Narrative Writer: Creating chapter summaries...")
                elif node_name == "brainstorming_narrative_critique":
                    print("🔍 Narrative Critique: Reviewing chapter summaries...")
                elif node_name == "writer":
                    chapter_count += 1
                    print(f"✍️  Writer: Writing Chapter {chapter_count}...")
                elif node_name == "writing_reviewer":
                    print(f"🔍 Reviewer: Reviewing Chapter {chapter_count}...")
                elif node_name == "assembler":
                    print("📚 Assembler: Compiling final book...")

        # Display results
        print("\n" + "="*60)
        print("🎉 BOOK CREATION COMPLETED!")
        print("="*60)

        if 'book_title' in node_state and node_state['book_title']:
            print(f"📖 Title: {node_state['book_title']}")

        if 'book_prologue' in node_state and node_state['book_prologue']:
            print(f"\n📜 Prologue:\n{node_state['book_prologue']}")

        if 'content' in node_state and node_state['content']:
            print(f"\n📚 Generated {len(node_state['content'])} chapters:")
            for i, (chapter_name, content) in enumerate(zip(node_state.get('chapter_names', []), node_state['content']), 1):
                print(f"\n--- Chapter {i}: {chapter_name} ---")
                print(content[:200] + "..." if len(content) > 200 else content)

        print(f"\n✅ Your book '{node_state.get('book_title', 'Untitled')}' is ready!")
        print("💡 Tip: Use 'python main.py gui' for a better interactive experience!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Book creation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during book creation: {str(e)}")
        print("💡 Make sure you have set up your API keys in a .env file.")
        sys.exit(1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Book Builder AI - Create books with AI agents")
    parser.add_argument(
        'mode',
        choices=['gui', 'cli'],
        nargs='?',
        default='gui',
        help='Run mode: gui (default) or cli'
    )

    args = parser.parse_args()

    if args.mode == 'gui':
        run_gui()
    else:
        run_cli()

if __name__ == "__main__":
    main()