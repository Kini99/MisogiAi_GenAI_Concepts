# Demo Screenshots and Usage Examples

This folder contains screenshots and examples demonstrating the AI Coding Agent Recommender system.

## Screenshots

### 1. Main Interface
- **File**: `main_interface.png`
- **Description**: Shows the main task input interface where users can enter their coding task description
- **Features**: Clean, modern UI with task input field and submit button

### 2. Task Analysis Results
- **File**: `task_analysis.png`
- **Description**: Displays the AI-powered task analysis showing extracted characteristics
- **Features**: Shows task type, complexity, languages, frameworks, and other extracted information

### 3. Agent Recommendations
- **File**: `recommendations.png`
- **Description**: Shows the top 3 recommended coding agents with scores and justifications
- **Features**: Ranked list with detailed explanations for each recommendation

### 4. Agent Database View
- **File**: `agents_database.png`
- **Description**: Displays all available coding agents and their capabilities
- **Features**: Comprehensive view of agent strengths, languages, frameworks, and pricing

## Usage Examples

### Example 1: Web Development Task
**Input**: "Build a React e-commerce website with payment integration"

**Expected Analysis**:
- Task Type: web_development
- Complexity: medium
- Languages: ["JavaScript", "TypeScript"]
- Frameworks: ["React", "Stripe"]
- Domain: web

**Expected Recommendations**:
1. Cursor (high score - excellent for React development)
2. GitHub Copilot (good for general web development)
3. Claude (strong reasoning for complex integrations)

### Example 2: Data Science Task
**Input**: "Create a machine learning model for customer churn prediction using Python"

**Expected Analysis**:
- Task Type: data_science
- Complexity: high
- Languages: ["Python"]
- Frameworks: ["scikit-learn", "pandas", "numpy"]
- Domain: data

**Expected Recommendations**:
1. Claude (excellent for complex ML tasks)
2. ChatGPT (strong in data science)
3. Kite (Python-focused)

### Example 3: Mobile Development Task
**Input**: "Develop a Flutter app for food delivery with real-time tracking"

**Expected Analysis**:
- Task Type: mobile_development
- Complexity: high
- Languages: ["Dart"]
- Frameworks: ["Flutter", "Firebase"]
- Domain: mobile

**Expected Recommendations**:
1. Cursor (excellent for complex mobile development)
2. Devin (end-to-end development capabilities)
3. GitHub Copilot (good for general development)

## How to Take Screenshots

1. Start the application: `python app.py`
2. Open browser and navigate to `http://localhost:5000`
3. Enter different task descriptions and capture the results
4. Save screenshots in this demo folder with descriptive names

## Notes

- The system uses Gemini 2.0 Flash for intelligent task analysis and agent recommendations
- All recommendations include detailed justifications explaining why each agent is suitable
- The system supports 12+ coding agents including Copilot, Cursor, Replit, CodeWhisperer, and more
- Fallback mechanisms ensure the system works even if Gemini API is unavailable 