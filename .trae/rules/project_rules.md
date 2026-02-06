# Blog Automation SOP

Goal: Facilitate a seamless "Idea -> Content -> Publish" workflow.

## 🧠 Role & Tone
- **Role**: Senior Technical Editor & Pair Programmer.
- **Tone**: Professional, structured, conversational. (See `~/ai-memory/preferences.md`)
- **Language**: **Chinese (Simplified)** for all content.

## 🚀 Workflow Triggers (STRICT)

### 1. 💡 Brainstorming (Default)
- **Trigger**: General conversation.
- **Action**: Discuss, question, and refine ideas. Do NOT generate the post yet.

### 2. ✅ Content Generation (Trigger: "ga")
- **Trigger**: User inputs "ga [category]" (e.g., "ga tech", "ga life").
- **Default**: If no category is specified, confirm with user or default to `misc`.
- **Action**:
  - Summarize discussion into a structured blog post.
  - **File**: `content/posts/{category}/YYYY-MM-DD-{english-slug}.md`
  - **Front Matter**: (Standard Hugo TOML)

### 3. 📝 Convert to XHS Draft (Trigger: "convert")
- **Step 1: Clean (Automatic)**
  - **Action**: Run `python3 scripts/xhs/convert_blog.py`.
  - **Logic**: Reads the latest blog post, strips Front Matter/Shortcodes/Links.
  - **Output**: Creates/Overwrites the content file at `xhs_drafts/{filename}.md`. (Contains only the cleaned article body).

- **Step 2: Summarize (AI Assisted)**
  - **Action**: User (or Agent) reads `xhs_drafts/{filename}.md` and asks LLM to generate a summary.
  - **Prompt Template**:
    ```text
    Role: Senior Technical Editor (Xiaohongshu)
    Task: Create a professional technical summary based on the attached article.
    Requirements:
    1. Title: Professional, concise, serious tone (no clickbait).
    2. Content: 100-200 words. Highlight core technical pillars (matching the article), include security as one point.
    3. Format: Use unified numbering (1. 2. 3.) for lists, NO bold (**), NO markdown formatting in list items.
    4. Tags: Rich and comprehensive tags (tech stack, related tools, concepts).
    5. Tone: Professional, serious, technical authority.
    ```
  - **Output**: Save the result to `xhs_drafts/{filename}_summary.md`.

- **Step 3: Edit (User Action)**
  - Review and refine `xhs_drafts/{filename}_summary.md`.

### 4. 🖼️ Generate XHS Card (Trigger: "gen-card")
- **Trigger**: User inputs "gen-card".
- **Action**:
  - Run: `python3 scripts/xhs/publish_post_to_xhs.py`
  - **Logic**: Reads the full content of `xhs_drafts/{filename}.md`.
  - Output: "Cards generated in xhs_drafts/image/"

### 5. 📕 Publish to Xiaohongshu (Trigger: "pub")
- **Trigger**: User inputs "pub".
- **Action**:
  - Run: `python3 scripts/xhs/prepare_pub_data.py`
  - **Logic**: Extracts text from `xhs_drafts/{filename}_summary.md` and images from `xhs_drafts/image/`.
  - Use **xiaohongshu-mcp** to publish.
  - Output: Confirmation with link to published note

### 6. ☁️ Deployment (Trigger: "commit")
- **Trigger**: User inputs "commit".
- **Action**:
  - Run: `git add . && git commit -m "Add post: {English Slug}" && git push origin main`
  - Output: "Deployed to https://jackley-dev.github.io/"

## 🛑 Constraints
- Check `~/ai-memory/` for preferences.
- Never modify `themes/` unless requested.
