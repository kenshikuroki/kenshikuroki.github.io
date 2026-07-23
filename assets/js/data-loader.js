// Enhanced data loader for publications and presentations with rich metadata
class EnhancedDataLoader {
  constructor() {
    this.publications = [];
    this.presentations = [];
  }

  escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  safeUrl(value) {
    if (typeof value !== 'string' || value.trim() === '') {
      return null;
    }
    try {
      const parsedUrl = new URL(value, window.location.href);
      return ['http:', 'https:'].includes(parsedUrl.protocol) ? parsedUrl.href : null;
    } catch {
      return null;
    }
  }

  safeToken(value, fallback = 'link') {
    const token = String(value ?? '').trim();
    return /^[a-z0-9_-]+$/i.test(token) ? token : fallback;
  }

  renderMath(container) {
    if (typeof renderMathInElement !== 'function' || !container) {
      return;
    }
    renderMathInElement(container, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false }
      ]
    });
  }

  async loadData() {
    try {
      // Load publications and presentations data
      const [publicationsResponse, presentationsResponse] = await Promise.all([
        fetch('./assets/data/publications.json'),
        fetch('./assets/data/presentations.json')
      ]);
      if (!publicationsResponse.ok || !presentationsResponse.ok) {
        throw new Error('Failed to load data files');
      }
      this.publications = await publicationsResponse.json();
      this.presentations = await presentationsResponse.json();
      // Render the sections
      this.renderPublications();
      this.renderPresentations();
      // Remove loading indicators
      document.getElementById('publications-loading')?.remove();
      document.getElementById('presentations-loading')?.remove();
      this.renderMath(document.getElementById('publications-container'));
      this.renderMath(document.getElementById('presentations-container'));
      window.navigationManager?.refreshSectionMetrics?.();
      window.navigationManager?.handleScroll?.();
    } catch (error) {
      console.error('Error loading data:', error);
      this.showErrorMessage();
      document.getElementById('publications-loading')?.remove();
      document.getElementById('presentations-loading')?.remove();
      window.navigationManager?.refreshSectionMetrics?.();
      window.navigationManager?.handleScroll?.();
    }
  }

  renderPublications() {
    const container = document.getElementById('publications-container');
    if (!container) return;
    let html = '';
    const linkPriority = { doi: 0, arxiv: 1 };
    this.publications.forEach(pub => {
      // Keep source data untouched and only normalize display order.
      const sortedLinks = [...(pub.links || [])].sort((a, b) => {
        const aPriority = linkPriority[a.type] ?? Number.MAX_SAFE_INTEGER;
        const bPriority = linkPriority[b.type] ?? Number.MAX_SAFE_INTEGER;
        return aPriority - bPriority;
      });
      const title = this.escapeHtml(pub.title);
      const authors = this.escapeHtml(pub.authors);
      const citations = Number.isFinite(pub.citations) ? pub.citations : 0;
      html += `
        <div class="card-item links">
          <div class="card-item-header">
            <h5 class="fw mb-0">${title}</h5>
            <span class="badge">${citations} citations</span>
          </div>
          <h6 class="mb-0">${authors}</h6>
          <h6 class="mb-0 publication-links-text">
            ${sortedLinks.map(link => {
              const safeUrl = this.safeUrl(link.url);
              if (!safeUrl) {
                return '';
              }
              const linkType = this.safeToken(link.type);
              const linkText = this.escapeHtml(link.text);
              return `
              <a href="${safeUrl}" target="_blank" rel="noopener noreferrer" class="link-item publication-link-inline" title="Access ${linkType}">
                <i class="ai ai-${linkType}"></i> ${linkText}
              </a>
            `;
            }).filter(Boolean).join('<br>')}
          </h6>
        </div>
      `;
    });
    container.innerHTML = html;
  }

  renderPresentations() {
    const container = document.getElementById('presentations-container');
    if (!container) return;
    let html = '';
    this.presentations.forEach(pres => {
      const pdfUrl = this.safeUrl(pres.url);
      const pdfLink = pdfUrl ?
        `<a href="${pdfUrl}" target="_blank" rel="noopener noreferrer" class="pdf-link pdf-link-inline" title="View PDF">
          <i class="fa-solid fa-file-pdf"></i>
        </a>` : '';
      // イベント名をリンク化
      const eventUrl = this.safeUrl(pres.event_url);
      const eventText = this.escapeHtml(pres.event);
      const eventHtml = eventUrl ?
        `<a href="${eventUrl}" target="_blank" rel="noopener noreferrer" class="event-link event-link-inline" title="Event Website">${eventText}</a>` :
        eventText;
      // Word Joiner (&#8288;) をカンマ直前に挿入し、カンマが行頭に来るのを防ぐ
      const title = this.escapeHtml(pres.title);
      const author = this.escapeHtml(pres.author);
      const location = this.escapeHtml(pres.location);
      const date = this.escapeHtml(pres.date);
      const type = this.escapeHtml(pres.type);
      html += `
        <div class="card-item links">
          <div class="card-item-header">
            <h5 class="fw mb-0">${title} ${pdfLink}</h5>
            <span class="badge">${type}</span>
          </div>
          <h6 class="mb-0">${author}</h6>
          <h6 class="mb-0 presentation-meta-text">
            ${eventHtml}<br>${location}&#8288;, ${date}
          </h6>
        </div>
      `;
    });
    container.innerHTML = html;
  }

  showErrorMessage() {
    const containers = [
      document.getElementById('publications-container'),
      document.getElementById('presentations-container')
    ];
    containers.forEach(container => {
      if (container) {
        container.innerHTML = `
          <div class="alert alert-warning" role="alert">
            <i class="fas fa-exclamation-triangle"></i>
            Unable to load content. Please refresh the page or contact the administrator.
          </div>
        `;
      }
    });
  }
}

// Global variable for access from HTML
let dataLoader;

// Initialize data loader when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  dataLoader = new EnhancedDataLoader();
  dataLoader.loadData();
});
