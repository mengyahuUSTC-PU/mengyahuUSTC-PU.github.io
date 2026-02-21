# Personal Website 🌐

A clean, modern personal portfolio for GitHub Pages. Built with plain HTML/CSS/JavaScript—no frameworks, just simplicity and style.

## 📁 Project Structure

```
.
├── index.html              # Main page
├── css/
│   └── style.css          # All styling
├── js/
│   └── main.js            # Dynamic content loading
├── data/
│   ├── posts.json         # Your blog posts
│   └── projects.json      # Your projects
├── images/                # Add your images here
└── README.md
```

## 🚀 How to Update Content

### ➕ Add a Blog Post

Edit `data/posts.json` and add a new object:

```json
{
    "title": "My Amazing Discovery",
    "date": "2025-02-21",
    "excerpt": "A brief summary of your thoughts...",
    "url": "https://example.com/full-post"  // optional
}
```

**Fields:**
- `title` (required): Post title
- `date` (required): Date in YYYY-MM-DD format
- `excerpt` (required): 1-2 sentence summary
- `url` (optional): Link to full post elsewhere

### ➕ Add a Project

Edit `data/projects.json` and add a new object:

```json
{
    "title": "Project Name",
    "emoji": "🚀",
    "description": "What this project does",
    "tags": ["Tag1", "Tag2"],
    "image": "images/project.jpg",
    "url": "https://github.com/..."
}
```

**Fields:**
- `title` (required): Project name
- `emoji` (optional): Single emoji, shows if no image
- `description` (required): What it does
- `tags` (optional): Array of skill/tech tags
- `image` (optional): Path to image (or leave empty to use emoji)
- `url` (optional): Link to GitHub, demo, or live site

## 🖼️ Adding Images

1. Create an `images/` folder in the root
2. Add your image files (JPG, PNG, etc.)
3. Reference them in your JSON:
   - `"image": "images/my-photo.jpg"`

## 🎨 Customizing the Design

Edit `css/style.css` to change colors, fonts, spacing, etc.

Key colors are defined at the top:
```css
:root {
    --primary-color: #2563eb;      /* Main blue */
    --secondary-color: #64748b;    /* Gray */
    --bg-color: #ffffff;           /* Background */
    /* etc */
}
```

## 📱 Responsive Design

The site works great on phones, tablets, and desktops. No changes needed—it's built in!

## 🌙 Dark Mode

Automatically respects your system's dark mode preference. No extra work required!

## 📤 Deploy to GitHub Pages

1. Create a repository named `mengyahuUSTC-PU.github.io`
2. Push these files to the repository
3. Your site goes live at `https://mengyahuUSTC-PU.github.io`

```bash
# In the repo directory
git add .
git commit -m "Initial website"
git push origin main
```

**That's it!** Updates take a few seconds to appear.

## 🛠️ Local Testing

Open `index.html` directly in your browser to preview. No build process needed!

**Note:** Some browsers block loading local JSON files from `file://` URLs. To test locally:

```bash
# Simple Python server (Python 3)
python -m http.server 8000

# Or Node.js
npx http-server
```

Then open `http://localhost:8000` in your browser.

## 📝 Tips

- Keep posts concise—the excerpt is what appears on the home page
- Use relative dates in posts (e.g., "Feb 21, 2025") for timeless feel
- Emoji in projects are fun—use relevant ones!
- Tags help readers understand what you worked with
- Links open in new tabs (projects only)

## ❓ FAQ

**Q: Can I add videos to posts/projects?**  
A: Not directly in the JSON, but you can link to external videos (YouTube, Vimeo) in the `url` field.

**Q: How do I add a contact form?**  
A: For now, you can add social links in the footer (edit `index.html`). Form handling would require a backend.

**Q: Can I use frameworks like React?**  
A: Yes! But this template is simpler without them. If you want React/Vue, that's a bigger refactor.

**Q: How do I change the site title?**  
A: Edit the `<title>` and `<h1>` in `index.html`.

---

Built with ❤️ for simplicity. Questions? Check the HTML/CSS/JS files—they're commented!
