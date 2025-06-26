# Kenshi KUROKI - Personal Academic Website

## 🌟 Features
- **Automated Citation Management**: Monthly auto-updates via INSPIRE-HEP database integration
- **Responsive Design**: Mobile-optimized using Bootstrap 5.3.0
- **SEO Optimized**: Schema.org structured data and Jekyll auto-generated sitemaps
- **Dynamic Content**: Asynchronous data loading with JavaScript


## 🏗️ Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.7.2, Academicons
- **Static Site Generator**: Jekyll
- **Automation**: GitHub Actions
- **Hosting**: GitHub Pages


## 📁 Project Structure
```
├── index.html                          # Main page
├── _config.yml                         # Jekyll configuration
├── assets/
│   ├── css/style.css                   # Custom styles
│   ├── js/
│   │   ├── navigation.js               # Navigation management
│   │   └── data-loader.js              # Data loading
│   ├── data/
│   │   ├── publications.json           # Publications data
│   │   └── presentations.json          # Presentations data
│   ├── images/profile.jpg              # Profile image
│   └── documents/CV_kuroki.pdf         # Curriculum Vitae
├── .github/workflows/
│   └── update-citations.yml            # Automated citation updates
├── scripts/
│   └── citation_updater.py             # Python citation update script
└── robots.txt                          # SEO configuration
```


## 🤖 Automation System

### Citation Management System
Automated citation update system running monthly:
- Fetches latest citation counts from INSPIRE-HEP API
- Comprehensive search strategies (ID, arXiv, DOI, title)
- Automatic backup and error handling
- GitHub Issues notifications for failures


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
  "url": "https://example.com/presentation"
}
```
### Updating Personal Information
Edit the following sections in `index.html`:
- Schema.org structured data (lines 18-58)
- Profile information (lines 110-156)
- Career and education information (lines 194-304)


## 📄 License
This project is for personal use. Please contact before reusing code.

## 📞 Contact
- **Email**: k-kuroki@impcas.ac.cn

---

© 2025 Kenshi Kuroki. All rights reserved.
