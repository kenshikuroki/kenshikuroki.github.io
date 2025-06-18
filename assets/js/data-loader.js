// Data loader for publications and presentations
class DataLoader {
  constructor() {
    this.publications = [];
    this.presentations = [];
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
      // ローディングインジケータを非表示に
      document.getElementById('publications-loading')?.remove();
      document.getElementById('presentations-loading')?.remove();
    } catch (error) {
      console.error('Error loading data:', error);
      // Fallback to show error message
      this.showErrorMessage();
      // ローディングインジケータを非表示に
      document.getElementById('publications-loading')?.remove();
      document.getElementById('presentations-loading')?.remove();
    }
  }
  renderPublications() {
    const container = document.getElementById('publications-container');
    if (!container) return;
    let html = '';
    this.publications.forEach(pub => {
      html += `
        <div class="card-item links">
          <div class="card-item-header">
            <h4 class="fw-bold mb-0">${pub.title}</h4>
            <span class="badge">${pub.citations} citations</span>
          </div>
          <p class="mb-0">${pub.authors}</p>
          ${pub.conference ? `
            <p class="mb-0" style="color: var(--text-muted)">
              ${pub.conference}<br>
              ${pub.location}, ${pub.date}
            </p>
          ` : ''}
          <p class="mb-0" style="color: var(--text-muted)">
            ${pub.links.map(link => `
              <a href="${link.url}" target="_blank">
                <i class="ai ai-${link.type}"></i> ${link.text}
              </a>
            `).join('\n            ')}
          </p>
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
      const pdfLink = pres.url ?
        `<a href="${pres.url}" target="_blank" class="pdf-link" title="View PDF" style="margin-left: 0.5rem; color: var(--text-muted); font-size: 1.5rem;">
        <i class="fa-solid fa-file-pdf"></i>
        </a>` : '';
      html += `
      <div class="card-item links">
        <div class="card-item-header">
          <h4 class="fw-bold mb-0">${pres.title} ${pdfLink}</h4>
          <span class="badge">${pres.type}</span>
        </div>
        <p class="mb-0">${pres.author}</p>
        <p class="mb-0" style="color: var(--text-muted)">
          ${pres.event} <br>
          ${pres.location}, ${pres.date}
        </p>
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

// Initialize data loader when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const dataLoader = new DataLoader();
  dataLoader.loadData();
});
