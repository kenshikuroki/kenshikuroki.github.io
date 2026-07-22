/**
* Navigation Manager
* スクロール連動ナビゲーションとスムーズスクロール機能を提供
*/
class NavigationManager {
  constructor(options = {}) {
    // デフォルト設定
    this.config = {
      navSelector: '.navbar-nav .nav-link',
      sectionSelector: 'section[id]',
      headerSelector: '.navbar',
      scrollOffset: 100,
      activeClass: 'active',
      ...options
    };
    this.navLinks = null;
    this.sections = null;
    this.sectionMetrics = [];
    this.header = null;
    this.isInitialized = false;
    this.scrollHandler = null;
    this.resizeHandler = null;
    // メソッドのバインド
    this.handleScroll = this.handleScroll.bind(this);
    this.handleNavClick = this.handleNavClick.bind(this);
    this.refreshSectionMetrics = this.refreshSectionMetrics.bind(this);
  }
  /**
  * 初期化
  */
  init() {
    if (this.isInitialized) {
      console.warn('NavigationManager is already initialized');
      return;
    }
    this.navLinks = document.querySelectorAll(this.config.navSelector);
    this.sections = document.querySelectorAll(this.config.sectionSelector);
    this.header = document.querySelector(this.config.headerSelector);
    if (this.navLinks.length === 0) {
      console.warn('No navigation links found');
      return;
    }
    if (this.sections.length === 0) {
      console.warn('No sections found');
      return;
    }
    this.refreshSectionMetrics();
    this.attachEventListeners();
    this.updateActiveLink(); // 初期状態の設定
    this.isInitialized = true;
  }
  /**
  * イベントリスナーの設定
  */
  attachEventListeners() {
    // スクロールイベント（パフォーマンス最適化のためthrottle）
    let ticking = false;
    this.scrollHandler = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          this.handleScroll();
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', this.scrollHandler, { passive: true });
    this.resizeHandler = () => {
      this.refreshSectionMetrics();
      this.handleScroll();
    };
    window.addEventListener('resize', this.resizeHandler, { passive: true });
    // ナビゲーションクリックイベント
    this.navLinks.forEach(link => {
      link.addEventListener('click', this.handleNavClick);
    });
  }

  refreshSectionMetrics() {
    this.sectionMetrics = Array.from(this.sections || []).map(section => ({
      id: section.getAttribute('id'),
      top: section.offsetTop,
      bottom: section.offsetTop + section.offsetHeight
    }));
  }
  /**
   * スクロールハンドラー
   */
  handleScroll() {
    this.updateActiveLink();
  }
  /**
   * アクティブリンクの更新
   */
  updateActiveLink() {
    const scrollPos = window.scrollY + this.config.scrollOffset;
    let currentSection = '';
    // 現在表示されているセクションをキャッシュ済み位置から特定
    for (const section of this.sectionMetrics) {
      if (scrollPos >= section.top && scrollPos < section.bottom) {
        currentSection = section.id;
        break;
      }
    }
    // ページ下部の場合、最後のセクションをアクティブに
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 10) {
      const lastSection = this.sectionMetrics[this.sectionMetrics.length - 1];
      if (lastSection) {
        currentSection = lastSection.id;
      }
    }
    // アクティブクラスの更新
    this.navLinks.forEach(link => {
      link.classList.remove(this.config.activeClass);
      const href = link.getAttribute('href');
      if (href === `#${currentSection}`) {
        link.classList.add(this.config.activeClass);
      }
    });
  }
  /**
   * ナビゲーションクリックハンドラー
   */
  handleNavClick(e) {
    const href = e.target.getAttribute('href');
    if (!href || !href.startsWith('#')) {
      return;
    }
    e.preventDefault();
    const target = document.querySelector(href);
    if (!target) {
      console.warn(`Target element not found: ${href}`);
      return;
    }
    this.scrollToSection(target);
  }
  /**
   * セクションへのスムーズスクロール
   */
  scrollToSection(target) {
    const headerHeight = this.header ? this.header.offsetHeight : 0;
    const targetPosition = target.offsetTop - headerHeight;
    window.scrollTo({
      top: targetPosition,
      behavior: 'smooth'
    });
  }
  /**
   * 設定の更新
   */
  updateConfig(newConfig) {
    this.config = { ...this.config, ...newConfig };
  }
  /**
   * 破棄（イベントリスナーの削除）
   */
  destroy() {
    if (!this.isInitialized) {
      return;
    }
    if (this.scrollHandler) {
      window.removeEventListener('scroll', this.scrollHandler);
      this.scrollHandler = null;
    }
    if (this.resizeHandler) {
      window.removeEventListener('resize', this.resizeHandler);
      this.resizeHandler = null;
    }
    if (this.navLinks) {
      this.navLinks.forEach(link => {
        link.removeEventListener('click', this.handleNavClick);
      });
    }
    this.isInitialized = false;
  }
}

// DOMContentLoaded時の自動初期化
document.addEventListener('DOMContentLoaded', () => {
  // target="_blank" のリンクに tabnabbing 対策を付与する
  document.querySelectorAll('a[target="_blank"]').forEach(link => {
    const relTokens = new Set((link.getAttribute('rel') || '').split(/\s+/).filter(Boolean));
    relTokens.add('noopener');
    relTokens.add('noreferrer');
    link.setAttribute('rel', Array.from(relTokens).join(' '));
  });
  // グローバルインスタンスの作成
  window.navigationManager = new NavigationManager();
  window.navigationManager.init();
});

// モジュールとしてもエクスポート（必要に応じて）
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NavigationManager;
}
