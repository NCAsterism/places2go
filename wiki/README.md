# Wiki Content

This directory contains all wiki page content for the Places2Go project.

## 📖 Available Pages

### Getting Started
- **Home.md** - Wiki homepage with navigation and project overview
- **Installation.md** - Complete installation guide
- **Quick-Start.md** - 5-minute quickstart tutorial

### Development
- **Development-Guide.md** - Comprehensive development documentation
- **Contributing.md** - How to contribute to the project
- **Architecture.md** - Technical architecture and design

### Additional Pages (To be created)
- Configuration.md - Configuration options
- Dashboard-Features.md - Feature documentation
- Testing.md - Testing guide
- Roadmap.md - Project roadmap
- FAQ.md - Frequently asked questions
- Troubleshooting.md - Common issues and solutions

## 🚀 Publishing to GitHub Wiki

### Method 1: Automated Script (Recommended)

**Prerequisites:**
1. Go to https://github.com/NCAsterism/places2go/wiki
2. Click "Create the first page"
3. Add any content (e.g., "Initial page")
4. Click "Save Page"

**Then run:**
```powershell
.\scripts\create_wiki.ps1
```

This will:
- Clone the wiki.git repository
- Copy all markdown files
- Commit and push to GitHub

### Method 2: Manual Copy-Paste

If the automated script doesn't work:

1. Go to https://github.com/NCAsterism/places2go/wiki
2. Click "New Page"
3. Copy content from each .md file in this directory
4. Paste into the wiki editor
5. Use the filename (without .md) as the page title
6. Save each page

### Method 3: Git Clone and Push

Once the wiki is initialized:

```bash
# From project root
cd ..
git clone https://github.com/NCAsterism/places2go.wiki.git
cd places2go.wiki

# Copy wiki files
cp ../places2go/wiki/*.md .

# Commit and push
git add .
git commit -m "docs: add comprehensive wiki documentation"
git push origin master
```

## 📝 Wiki Page Naming Convention

GitHub wiki pages use specific naming:
- Spaces become dashes: "Quick Start" → "Quick-Start.md"
- Home page is always "Home.md"
- Case-sensitive on some systems

## 🔗 Internal Links

Wiki pages use relative links:
```markdown
[Development Guide](Development-Guide)
[Quick Start](Quick-Start)
```

## ✏️ Editing Wiki Content

1. Edit markdown files in this `wiki/` directory
2. Run the publishing script to update GitHub
3. Or manually update via GitHub web interface

## 📦 Wiki Structure

```
wiki/
├── README.md              (this file)
├── Home.md                (homepage)
├── Installation.md        (installation guide)
├── Quick-Start.md         (quickstart)
├── Development-Guide.md   (dev docs)
├── Contributing.md        (contribution guide)
└── Architecture.md        (architecture overview)
```

## 🎯 Best Practices

- Keep pages focused and concise
- Use clear headings for navigation
- Include code examples where appropriate
- Link related pages together
- Update table of contents in Home.md when adding pages

## 🐛 Troubleshooting

**Wiki.git repository not found?**
- The wiki must be initialized via GitHub UI first
- Create at least one page manually via the web interface

**Permission denied when pushing?**
- Ensure you're authenticated: `gh auth status`
- Check repository access rights

**Changes not appearing?**
- Wiki updates may take a few seconds to reflect
- Hard refresh your browser (Ctrl+F5)

## 📚 Resources

- [GitHub Wiki Documentation](https://docs.github.com/en/communities/documenting-your-project-with-wikis)
- [Markdown Guide](https://www.markdownguide.org/)
- [Project Repository](https://github.com/NCAsterism/places2go)

---

**Last Updated:** October 4, 2025
