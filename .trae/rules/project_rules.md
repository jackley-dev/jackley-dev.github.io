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
    - **Slug**: MUST explicitly set `slug = "{english-slug}"` to ensure clean URLs and avoid index issues caused by Chinese titles.
    - **Taxonomies**: MUST use flat format (e.g., `tags = [...]`, `categories = ["tech"]`). Do NOT use `[taxonomies]` as it causes parsing errors in some Hugo themes.
    - **Date/Time**: MUST set the time to `00:00:00+08:00` (e.g., `YYYY-MM-DDT00:00:00+08:00`). If set to current time, GitHub Actions (UTC timezone) might consider it a "future" time and skip building the post.
  - **Writing Style (Strict)**:
    1. **极简直白 (Minimalist & Direct)**：结论先行，直奔主题。拒绝抒情、口水话和空洞的隐喻（如“软件 2.0”），背景描述要口语化、接地气。
    2. **高度结构化 (Structured)**：多用列表、对比表格、文件树 (Tree) 展示逻辑，保证内容一目了然，极具扫读性。
    3. **极客用词 (Geeky & Professional)**：术语精准，边界清晰。作为“高级工程师给自己的踩坑备忘录”，注重痛点解决和实操性（直接给出命令/代码）。
    4. **Image Paths**: MUST use absolute path from the root (e.g., `/images/xxx.jpg`). Do NOT use relative paths like `../../../static/images/`. The IDE preview works with `/images/` because of the `images -> static/images` symlink in the project root.

### 3. 📝 Convert to XHS Draft (Trigger: "convert")
- **Step 1: Clean (Automatic)**
  - **Action**: Run `python3 scripts/xhs/convert_blog.py`.
  - **Logic**: Reads the latest blog post, strips Front Matter/Shortcodes/Links.
  - **Output**: Creates/Overwrites the content file at `xhs_drafts/files/{filename}.md`. (Contains only the cleaned article body).

- **Step 2: Summarize (AI Assisted)**
  - **Action**: User (or Agent) reads `xhs_drafts/files/{filename}.md` and asks LLM to generate a summary.
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
  - **Output**: Save the result to `xhs_drafts/files/{filename}_summary.md`.

- **Step 3: Edit (User Action)**
  - Review and refine `xhs_drafts/files/{filename}_summary.md`.

### 4. 🖼️ Generate XHS Card
#### Option A: Plain Text (Trigger: "gen-card")
- **Trigger**: User inputs "gen-card".
- **Action**:
  - Run: `python3 scripts/xhs/publish_post_to_xhs.py`
  - **Logic**: Simple text-based generation using PIL. Best for simple news/quotes.
  - Output: "Cards generated in xhs_drafts/images/"

#### Option B: Rich Content (Trigger: "gen-rich")
- **Trigger**: User inputs "gen-rich".
- **Action**:
  - Run: `python3 scripts/xhs/publish_post_to_xhs.py -m render`
  - **Logic**: HTML/CSS based rendering with Playwright. Supports Code blocks, Tables, Images, Notion-style layout.
  - Output: "Cards generated in xhs_drafts/images/"

### 5. 📕 Publish to Xiaohongshu (Trigger: "pub")
- **Trigger**: User inputs "pub".
- **Action**:
  - Run: `python3 scripts/xhs/prepare_pub_data.py`
  - **Logic**: Extracts text from `xhs_drafts/files/{filename}_summary.md` and images from `xhs_drafts/images/`.
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
- **Output Quality Control**: Ensure all generated files use standard UTF-8 encoding. STRICTLY PROHIBIT the use of Zero Width Space (\u200b), Non-breaking Space (\u00a0), or other invisible control characters. Use standard space (0x20) and newline (\n) only.
- **Content Formatting**:
  - Do NOT use `<!--more-->` tag in blog posts. Rely on Hugo's automatic summary or `description` front matter field.
  - **Header Levels**: Use H2 (##) for main sections and H3 (###) for subsections. Avoid using H4 (####) or deeper to ensure better compatibility with XHS card generation (font size issues).
