# Book Builder With AI

**Imagine your story or adventure and make it a reality with Book Builder With AI.**

This software empowers you to create an entire book tailored to your interests or suggestions. Leveraging an AI-based Autonomous Agents Architecture, the process is highly customizable to ensure your story is crafted exactly as you envision it.

## ✨ NEW FEATURES

- 🚀 **OpenRouter Support**: Use any model available through OpenRouter API
- 🎨 **Beautiful GUI**: Interactive web interface built with Streamlit
- 💬 **Real-time Chat**: Interactive feedback system with AI agents
- 📊 **Progress Visualization**: Visual progress tracking during book creation
- 📤 **Multiple Export Formats**: Export your book as TXT, JSON, or Markdown
- 🌐 **Multi-language Support**: 20+ languages supported
- 🔧 **Flexible Configuration**: Customize every aspect of your book creation

## 🚀 QUICK START

### Option 1: GUI Version (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Launch the GUI
python main.py gui
```

Then open your browser to `http://localhost:8501` to access the Book Builder interface!

### Option 2: CLI Version (Original)

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Run CLI version
python main.py cli
```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure your API keys:

```bash
# OpenAI API Key (required for OpenAI models)
OPENAI_API_KEY=your_openai_api_key_here

# Google AI API Key (required for Google models)
GOOGLE_API_KEY=your_google_api_key_here

# Groq API Key (required for Meta and DeepSeek models)
GROQ_API_KEY=your_groq_api_key_here

# AWS Bedrock credentials (required for Amazon models)
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION_NAME=us-east-1

# OpenRouter API Key (required for OpenRouter models)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct
```

### Supported AI Models

- **OpenAI**: `gpt-4o-mini` (via OpenAI API)
- **Google**: `gemini-exp-1206` (via Google AI API)
- **Meta**: `llama-3.3-70b-versatile` (via Groq)
- **DeepSeek**: `deepseek-r1-distill-llama-70b` (via Groq)
- **Amazon**: `anthropic.claude-3-5-sonnet-20240620-v1:0` (via AWS Bedrock)
- **OpenRouter**: Configurable via `OPENROUTER_MODEL` in `.env` file (supports 1000+ models!)

## HOW IT WORKS

### Overview:
Book Builder With AI follows a systematic, interactive workflow that guides you from your initial concept to a fully developed book. Here's how the process unfolds:

<img width="440" alt="image" src="https://github.com/user-attachments/assets/d7bafcd2-0d71-4ea2-841b-7da451c400d8">



### 1. **Initiation by the Human:**
You kickstart the AI workflow by providing an initial message about your book idea. This could include a rough concept, genre, specific themes, or any other guidance you want to provide.

### 2. **Instructor Agent:**
The Instructor Agent takes your initial input and begins documenting the requirements for your book. The agent might ask you further questions to refine the concept and ensure it fully understands your vision. This phase can involve multiple iterations until the Instructor has a clear and complete set of instructions.

### 3. **Brainstorming Idea Writer:**
Once the instructions are finalized, they are handed over to the Brainstorming Idea Writer Agent. This agent is responsible for drafting a detailed outline of your book, considering the following key elements:
- **Story Overview:** A highly detailed overview of the narrative that includes a strong introduction, a well-developed middle, and a satisfying conclusion.
- **Characters:**  Characters of the story descriptions: background, motivations, and situations along the story journey.
- **Writing Style:**  The style and tone the writer should consider while developing the book.
- **Book Name:** The title of the book. 
- **Book Prologue:** The opening section of the book.
- **Context Setting:**  The time, place, and atmosphere where the story takes place. 
- **Inciting Incident:** The event that disrupts the protagonist’s normal life and initiates the main plot.
- **Themes Conflict Intro:**  The central themes and conflicts that will be explored in the story. 
- **Transition to Development:**  A transition from the Introduction to the Development stage. 
- **Rising Action:**  The key events that increase tension and advance the central conflict.
- **SubPlots:** Any secondary storylines that complement the main plot. 
- **Midpoint:** A significant event that alters the direction of the story or escalates the conflict. 
- **Climax Build Up:** The events leading up to the climax. 
- **Climax:** The decisive moment where the main conflict reaches its peak. 
- **Falling Action:** The immediate aftermath of the climax.
- **Resolution:** Conclusion fo the story.
- **Epilogue:** A final reflection or glimpse into the characters' future, showing the long-term impact of the story.


### 4. **Critique and Refinement:**
After the initial draft is developed, a Critique Agent reviews it and suggests adjustments. The Brainstorming Idea Writer then revises the draft based on this feedback. This cycle continues until the Critique Agent approves the draft.

### 5. **Developing Deeply Narratives:**
With the draft approved, the final version is passed to the Brainstorming Narrative Writer Agent. This agent will generate a summary of each of the chapter the book will have.


### 5. **New Critiques and Refinements:**
When the narrative is developed, it will be reviewed by the Brainstorming Narrative Critique Agent. It will make a review of the narrative and provide feedback. Then the Brainstorming Narrator Writer will make the adjustments. This cycle continues until the Critique Agent approves the draft.

### 6. **Writing the Book:**
When it is approved the draft of the Brainstorming Narrative Writer, it is time to start writing the entire book. This Writer agent develops the full book, chapter by chapter, following the established requirements.

### 6. **Chapter-by-Chapter Review:**
As each chapter is completed, a Reviewer Agent analyzes it and provides feedback for improvements. The Writer adapts the chapter based on this feedback, and the process repeats until the Reviewer approves the chapter.

### 7. **Translation if needed:**
Once all chapters are written and approved, based on the initial configuration, the book is translated (or not) to a target language.


### 8. **Completion:**
We finally execute the assembler node, which gathers and prepares the book for reading. The finished product includes the book title, prologue, used_models, how was the user requirements and the complete content of your story, ready for you to enjoy or share with others.


## 🎨 GUI Features

The new GUI provides:

- **📊 Visual Progress Tracking**: See real-time progress through each stage
- **💬 Interactive Chat**: Communicate with AI agents during the process
- **⚙️ Configuration Panel**: Easy setup of all book parameters
- **📤 Export Options**: Download books in TXT, JSON, or Markdown format
- **📚 Book Preview**: Preview completed chapters before export
- **🌐 Multi-language Interface**: Interface available in multiple languages

## 📖 Usage Examples

### Example Book Idea:
> "Write a science fiction thriller about a detective who discovers a conspiracy involving advanced AI technology that threatens humanity. The story should be fast-paced with lots of action and plot twists."

### GUI Workflow:
1. Open the application in your browser
2. Configure your book settings in the sidebar
3. Enter your book idea in the main area
4. Click "Start Creating Book"
5. Interact with AI agents through the chat interface
6. Monitor progress with the visual indicator
7. Export your completed book

## 🔧 Advanced Configuration

For more control over the book creation process, you can:

- **Customize Prompts**: Modify the agent prompts in `src/constants.py`
- **Add New Models**: Extend the model support in `src/utils.py`
- **Modify Workflow**: Adjust the agent workflow in `src/agent.py`
- **Add Languages**: Extend language support in the configuration

### Project Structure:
```
├── src/
│   ├── agent.py          # Main LangGraph workflow
│   ├── constants.py      # AI agent prompts and configurations
│   ├── gui.py           # Streamlit GUI application
│   ├── nodes.py         # Individual agent implementations
│   ├── routers.py       # Workflow routing logic
│   └── utils.py         # Utility functions and data models
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

---

**Book Builder With AI** is designed to bring your ideas to life through a collaborative process with AI, ensuring your story is as close to your vision as possible. Happy writing!