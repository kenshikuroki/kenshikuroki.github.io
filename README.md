# Kenshi KUROKI - Personal Academic Website

## 🌟 Features

- **Automated Citation Management**: Monthly auto-updates via INSPIRE-HEP database integration
- **Responsive Design**: Mobile-optimized using Bootstrap 5.3.0
- **SEO Optimized**: Schema.org structured data and sitemap
- **Dynamic Content**: Asynchronous data loading with JavaScript


## 🏗️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.7.2, Academicons
- **Automation**: GitHub Actions
- **Hosting**: GitHub Pages


## 📁 Project Structure

```plaintext
├── index.html                          # Main page
├── assets/
│   ├── css/style.css                   # Custom styles
│   ├── js/
│   │   ├── navigation.js               # Navigation management
│   │   └── data-loader.js              # Data loading
│   ├── data/
│   │   ├── publications.json           # Publications data
│   │   └── presentations.json          # Presentations data
│   └── images/
│       └── profile.jpg                 # Profile image
├── .github/workflows/
│   └── update-citations.yml            # Automated citation updates
│   └── update-sitemap.yml              # Automated sitemap generation
├── scripts/
│   └── citation_updater.py             # Python citation update script
│   └── generate_sitemap.py             # Python sitemap generation script
├── sitemap.xml                         # Automatically generated sitemap
└── robots.txt                          # SEO configuration
```


## 🤖 Automation System

### Repository Access Policy

- Use SSH remote URLs for this repository (recommended for workflow file updates).
- HTTPS + PAT can be used only when the token has `workflow` scope.
- If push fails while editing `.github/workflows/*.yml`, verify the protocol first with `git remote -v`.

### Citation Management System

Automated citation update system running monthly:

- Uses `scripts/citation_updater.py` to fetch and update citations
- Fetches latest citation counts from INSPIRE-HEP API
- Comprehensive search strategies (ID, arXiv, DOI, title)
- Automatic backup and error handling
- GitHub Issues notifications for failures

### Sitemap Generation

Automatically generates `sitemap.xml`:

- Uses `scripts/generate_sitemap.py` for generation
- Includes pages and data files
- Updates on every push to the repository


## 🚀 Updates

### Adding Publications

Add new publications to `assets/data/publications.json`:

```json
{
  "title": "Paper Title",
  "authors": "Author Names",
  "inspire_id": "INSPIRE-HEP ID"
}
```

The script, `scripts/citation_updater.py`, will automatically retrieve additional information from INSPIRE-HEP.
To update the data immediately, run the script manually from GitHub Actions with the dry run option set to false.

### Adding Presentations

Add new presentations to `assets/data/presentations.json`:

```json
{
  "title": "Presentation Title",
  "event": "Conference Name",
  "type": "Invited Talk",
  "location": "Location",
  "date": "2025-01-01",
  "url": "URL to Presentation Slides (if available)"
}
```


## 📄 License

This project is for personal use. Please contact before reusing code.


## 📞 Contact

- **Email**: [k-kuroki-e23@eagle.sophia.ac.jp](mailto:k-kuroki-e23@eagle.sophia.ac.jp)


## 🧪 SEO Validation Checklist

- Validate structured data in [Google Rich Results Test](https://search.google.com/test/rich-results).
- Validate [sitemap.xml](sitemap.xml) after major content updates.
- Ensure [robots.txt](robots.txt) points to the latest sitemap URL.


---

© 2026 Kenshi Kuroki. All rights reserved.
