import streamlit as st
import asyncio
import json
import os
import threading
import time
from datetime import datetime
from typing import Dict, Any, List
import plotly.graph_objects as go
from src.agent import app, workflow
from src.utils import State
from langchain_core.messages import HumanMessage
import pandas as pd


class BookBuilderGUI:
    def __init__(self):
        self.config = {}
        self.current_stage = "setup"
        self.book_content = []
        self.chapter_names = []
        self.current_chapter = 0
        self.is_processing = False
        self.progress_messages = []
        # Create GUI-specific app without interrupts
        self.app = workflow.compile()

    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        st.sidebar.title("📚 Book Builder AI")
        st.sidebar.markdown("---")

        # Language selection
        st.sidebar.subheader("🌐 Language Settings")
        self.config['language'] = st.sidebar.selectbox(
            "Target Language",
            ['english', 'spanish', 'portuguese', 'poland', 'french', 'german',
             'italian', 'dutch', 'swedish', 'norwegian', 'danish', 'finnish',
             'russian', 'chinese', 'japanese', 'korean', 'arabic', 'turkish',
             'greek', 'hebrew'],
            index=0
        )

        # Model configuration (OpenRouter only)
        st.sidebar.subheader("🤖 AI Model Configuration")
        st.sidebar.info("🎯 Using OpenRouter models for all agents")
        
        with st.sidebar.expander("ℹ️ OpenRouter Setup"):
            st.markdown("""
            **Environment Variables Required:**
            - `OPENROUTER_API_KEY`: Your OpenRouter API key
            - `OPENROUTER_MODEL`: Model to use (default: meta-llama/llama-3.2-3b-instruct)
            - `OPENROUTER_BASE_URL`: API base URL (default: https://openrouter.ai/api/v1)
            """)
        
        # Set all models to openrouter
        self.config['instructor_model'] = 'openrouter'
        self.config['brainstormer_idea_model'] = 'openrouter'
        self.config['brainstormer_critique_model'] = 'openrouter'
        self.config['writer_model'] = 'openrouter'
        self.config['writing_reviewer_model'] = 'openrouter'
        self.config['translator_model'] = 'openrouter'

        # Book parameters
        st.sidebar.subheader("📖 Book Configuration")
        self.config['n_chapters'] = st.sidebar.slider("Number of Chapters", 3, 20, 8)
        self.config['min_paragraph_per_chapter'] = st.sidebar.slider(
            "Min Paragraphs per Chapter", 3, 15, 5
        )
        self.config['min_sentences_in_each_paragraph_per_chapter'] = st.sidebar.slider(
            "Min Sentences per Paragraph", 3, 10, 5
        )
        self.config['critiques_in_loop'] = st.sidebar.checkbox(
            "Enable Critique Loops", value=False
        )

        # Action buttons
        st.sidebar.markdown("---")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🚀 Start New Book", use_container_width=True):
                st.session_state.current_stage = "instructor"
                st.rerun()
        with col2:
            if st.button("📤 Export Book", use_container_width=True, disabled=len(self.book_content) == 0):
                self.export_book()

    def render_progress_indicator(self):
        """Render the progress visualization"""
        stages = [
            ("setup", "⚙️ Setup"),
            ("instructor", "👨‍🏫 Instructor"),
            ("brainstorming", "💡 Brainstorming"),
            ("writing", "✍️ Writing"),
            ("review", "🔍 Review"),
            ("translation", "🌍 Translation"),
            ("complete", "✅ Complete")
        ]

        stage_idx = ["setup", "instructor", "brainstorming", "writing", "review", "translation", "complete"].index(self.current_stage)

        fig = go.Figure()

        for i, (stage_id, stage_name) in enumerate(stages):
            color = "green" if i <= stage_idx else "lightgray"
            showlabel = i == stage_idx

            fig.add_trace(go.Scatter(
                x=[i], y=[0],
                mode='markers+text',
                marker=dict(size=20, color=color),
                text=stage_name if showlabel else "",
                textposition="top center",
                showlegend=False
            ))

        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=20),
            height=100
        )

        st.plotly_chart(fig, use_container_width=True)

    def render_chat_interface(self):
        """Render the chat interface for human feedback"""
        st.subheader("💬 Interactive Book Creation")

        # Display current stage info
        stage_info = {
            "instructor": "👨‍🏫 **Instructor Agent** - Refining your book requirements",
            "brainstorming": "💡 **Brainstorming Agent** - Creating story outline",
            "writing": "✍️ **Writer Agent** - Writing chapters",
            "review": "🔍 **Reviewer Agent** - Reviewing content",
            "translation": "🌍 **Translator Agent** - Translating content"
        }

        if self.current_stage in stage_info:
            st.info(stage_info[self.current_stage])

        # Chat messages
        chat_container = st.container()
        with chat_container:
            if 'messages' not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        # Chat input
        if not self.is_processing:
            user_input = st.chat_input("Enter your response or feedback...")

            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.rerun()

    def export_book(self):
        """Export the completed book"""
        if not self.book_content:
            st.error("No book content to export!")
            return

        # Create book data
        book_data = {
            "title": st.session_state.get('book_title', 'Untitled Book'),
            "prologue": st.session_state.get('book_prologue', ''),
            "chapters": [
                {"name": name, "content": content}
                for name, content in zip(self.chapter_names, self.book_content)
            ],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "language": self.config.get('language', 'english'),
                "total_chapters": len(self.book_content)
            }
        }

        # Export options
        export_format = st.selectbox(
            "Export Format",
            ["TXT", "JSON", "MD"],
            key="export_format"
        )

        if export_format == "TXT":
            content = self._format_book_txt(book_data)
            filename = f"{book_data['title'].replace(' ', '_')}.txt"
        elif export_format == "JSON":
            content = json.dumps(book_data, indent=2, ensure_ascii=False)
            filename = f"{book_data['title'].replace(' ', '_')}.json"
        else:  # MD
            content = self._format_book_md(book_data)
            filename = f"{book_data['title'].replace(' ', '_')}.md"

        st.download_button(
            label=f"📥 Download {export_format}",
            data=content,
            file_name=filename,
            mime="text/plain" if export_format != "JSON" else "application/json",
            use_container_width=True
        )

    def _format_book_txt(self, book_data):
        """Format book as plain text"""
        lines = []
        lines.append(f"Title: {book_data['title']}")
        lines.append("=" * len(book_data['title']))
        lines.append("")
        if book_data['prologue']:
            lines.append("PROLOGUE")
            lines.append("-" * 8)
            lines.append(book_data['prologue'])
            lines.append("")

        for i, chapter in enumerate(book_data['chapters'], 1):
            lines.append(f"CHAPTER {i}: {chapter['name']}")
            lines.append("-" * (len(f"CHAPTER {i}: {chapter['name']}")))
            lines.append(chapter['content'])
            lines.append("")

        return "\n".join(lines)

    def _format_book_md(self, book_data):
        """Format book as Markdown"""
        lines = []
        lines.append(f"# {book_data['title']}")
        lines.append("")

        if book_data['prologue']:
            lines.append("## Prologue")
            lines.append("")
            lines.append(book_data['prologue'])
            lines.append("")

        for i, chapter in enumerate(book_data['chapters'], 1):
            lines.append(f"## Chapter {i}: {chapter['name']}")
            lines.append("")
            lines.append(chapter['content'])
            lines.append("")

        return "\n".join(lines)

    def run_book_creation(self):
        """Run the book creation process"""
        if not hasattr(st.session_state, 'user_input'):
            st.error("Please enter your book idea first!")
            return

        self.is_processing = True
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Initialize the graph with configuration
            graph_config = {
                'configurable': self.config,
                'recursion_limit': 50  # Increase recursion limit for complex book generation
            }

            # Create initial state
            state = {
                'content': [],
                'translated_content': [],
                'translated_chapter_names': [],
                'content_of_approved_chapters': [],
                'chapter_names_of_approved_chapters': [],
                'chapter_names': [],
                'writer_memory': [],
                'translator_memory': [],
                'user_instructor_messages': [HumanMessage(content=st.session_state.user_input)],
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

            # Initialize final state
            final_state = None

            # Initialize chapter counter for CLI-like messages
            chapter_count = 0

            # Run the graph
            for event in self.app.stream(state, graph_config):
                for node_name, node_state in event.items():
                    final_state = node_state  # Keep track of the latest state

                    if node_name == "instructor":
                        status_text.text("👨‍🏫 Instructor Agent: Gathering and refining requirements...")
                        progress_bar.progress(10)

                    elif node_name == "brainstorming_idea_writer":
                        status_text.text("💡 Brainstorming Agent: Creating story outline...")
                        progress_bar.progress(20)

                    elif node_name == "brainstorming_idea_critique":
                        status_text.text("🔍 Brainstorming Critique: Reviewing story outline...")
                        progress_bar.progress(25)

                    elif node_name == "brainstorming_narrative_writer":
                        status_text.text("📝 Narrative Writer: Creating chapter summaries...")
                        progress_bar.progress(30)

                    elif node_name == "brainstorming_narrative_critique":
                        status_text.text("🔍 Narrative Critique: Reviewing chapter summaries...")
                        progress_bar.progress(35)

                    elif node_name == "writer":
                        chapter_count += 1
                        status_text.text(f"✍️ Writer: Writing Chapter {chapter_count}...")
                        progress_bar.progress(40 + (chapter_count / self.config['n_chapters']) * 30)

                    elif node_name == "writing_reviewer":
                        status_text.text(f"🔍 Reviewer: Reviewing Chapter {chapter_count}...")
                        progress_bar.progress(45 + (chapter_count / self.config['n_chapters']) * 30)

                    elif node_name == "translator":
                        status_text.text("🌍 Translator: Translating content...")
                        progress_bar.progress(85)

                    elif node_name == "assembler":
                        status_text.text("📚 Assembler: Compiling final book...")
                        progress_bar.progress(95)

            # Update session state with results
            if final_state and 'content' in final_state:
                st.session_state.book_content = final_state['content']
                st.session_state.book_title = final_state.get('book_title', 'Untitled Book')
                st.session_state.book_prologue = final_state.get('book_prologue', '')

            self.current_stage = "complete"
            progress_bar.progress(100)
            status_text.text("✅ Book creation completed!")

            # Add completion message to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🎉 Your book has been successfully created! You can now export it using the sidebar."
            })

        except Exception as e:
            st.error(f"Error during book creation: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ Error: {str(e)}"
            })
        finally:
            self.is_processing = False

    def render_main_content(self):
        """Render the main content area"""
        st.title("📚 Book Builder AI")

        # Progress indicator
        self.render_progress_indicator()

        # Main content based on current stage
        if self.current_stage == "setup":
            self.render_setup()
        elif self.current_stage in ["instructor", "brainstorming", "writing", "review", "translation"]:
            self.render_chat_interface()
        elif self.current_stage == "complete":
            self.render_book_preview()

    def render_setup(self):
        """Render the initial setup screen"""
        st.markdown("""
        ## Welcome to Book Builder AI! 🚀

        This application uses AI agents to create complete books based on your ideas.
        All agents are powered by **OpenRouter** models for consistent, high-quality results!

        ### Features:
        - 🤖 OpenRouter AI models for all agents (instructor, brainstormer, writer, reviewer, translator)
        - 🌐 Multi-language support (20+ languages)
        - 📖 Customizable book structure
        - 💬 Interactive feedback system
        - 📤 Export in multiple formats (TXT, JSON, Markdown)

        ### How it works:
        1. **Setup**: Configure your book parameters in the sidebar
        2. **Instructor**: AI gathers and refines your requirements
        3. **Brainstorming**: AI creates story outline and structure
        4. **Writing**: AI writes chapters with your feedback
        5. **Review**: AI reviews and improves content
        6. **Translation**: Optional translation to target language
        7. **Export**: Download your completed book

        ---
        """)

        st.subheader("📝 Enter Your Book Idea")
        
        # Initialize session state for user_input if it doesn't exist
        if 'user_input' not in st.session_state:
            st.session_state.user_input = ""
            
        user_input = st.text_area(
            "Describe your book idea, genre, characters, or any specific requirements:",
            placeholder="Example: Write a science fiction thriller about a detective who discovers a conspiracy involving advanced AI technology that threatens humanity...",
            height=150,
            value=st.session_state.user_input,
            key="book_idea_input"
        )

        if st.button("🚀 Start Creating Book", type="primary", use_container_width=True):
            if user_input.strip():
                st.session_state.user_input = user_input
                st.session_state.current_stage = "instructor"
                st.success("Starting book creation process...")
                st.rerun()
            else:
                st.error("Please enter your book idea first!")

    def render_book_preview(self):
        """Render the completed book preview"""
        st.success("🎉 Your book has been successfully created!")

        if hasattr(st.session_state, 'book_title') and st.session_state.book_title:
            st.subheader(f"📖 {st.session_state.book_title}")

        if hasattr(st.session_state, 'book_prologue') and st.session_state.book_prologue:
            with st.expander("📜 Prologue"):
                st.write(st.session_state.book_prologue)

        if hasattr(st.session_state, 'book_content') and st.session_state.book_content:
            st.subheader("📚 Chapters")

            for i, (chapter_name, chapter_content) in enumerate(zip(self.chapter_names, st.session_state.book_content), 1):
                with st.expander(f"Chapter {i}: {chapter_name}"):
                    st.write(chapter_content)

        # Export section
        st.markdown("---")
        st.subheader("📤 Export Your Book")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Export as TXT", use_container_width=True):
                self.export_book()
        with col2:
            if st.button("📋 Export as JSON", use_container_width=True):
                self.export_book()
        with col3:
            if st.button("📄 Export as Markdown", use_container_width=True):
                self.export_book()


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Book Builder AI",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = "setup"

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Create GUI instance
    gui = BookBuilderGUI()

    # Render sidebar
    gui.render_sidebar()

    # Render main content
    gui.render_main_content()


if __name__ == "__main__":
    main()
