#!/usr/bin/env python3

import datetime
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

class SitemapGenerator:
  def __init__(self, base_url="https://kenshikuroki.github.io"):
    self.base_url = base_url
    self.urls = []
    self.repo_root = Path(__file__).resolve().parent.parent
    self.lastmod_source_file = 'index.html'
    self.lastmod_source_value = ''

  def repo_path(self, relative_path):
    return self.repo_root / relative_path

  def add_url(self, loc, lastmod=None, changefreq="monthly", priority="0.5"):
    """Add URL to sitemap"""
    normalized_loc = loc if loc.startswith('/') else f'/{loc}'
    url_data = {
      'loc': f"{self.base_url}{normalized_loc}",
      'lastmod': lastmod or datetime.datetime.now().strftime('%Y-%m-%d'),
      'changefreq': changefreq,
      'priority': priority
    }
    self.urls.append(url_data)

  def get_file_modification_date(self, filepath):
    """Get the file's last modification date from git history."""
    file_path = self.repo_path(filepath)
    try:
      result = subprocess.run(
        ["git", "log", "-1", "--format=%cd", "--date=short", "--", str(filepath)],
        cwd=self.repo_root,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
      )
      date_str = result.stdout.strip()
      if date_str:
        return date_str
    except (subprocess.SubprocessError, OSError) as e:
      print(f"git log failed for {filepath}: {e}")

    # Fallback: use filesystem mtime only when git history is unavailable.
    if file_path.exists():
      timestamp = file_path.stat().st_mtime
      return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    return datetime.datetime.now().strftime('%Y-%m-%d')

  def scan_important_files(self):
    """Scan and add important files to sitemap"""
    self.urls = []
    # Main page
    index_lastmod = self.get_file_modification_date('index.html')
    self.add_url('/', index_lastmod, 'monthly', '1.0')
    # Data files (for SEO if they change frequently)
    data_files = [
      'assets/data/publications.json',
      'assets/data/presentations.json'
    ]
    newest_lastmod = index_lastmod
    newest_source_file = 'index.html'
    for data_file in data_files:
      if self.repo_path(data_file).exists():
        lastmod = self.get_file_modification_date(data_file)
        # Don't include JSON files in sitemap as they're not directly accessible
        # But use their modification time to update main page lastmod
        if lastmod > newest_lastmod:
          newest_lastmod = lastmod
          newest_source_file = data_file
    self.urls[0]['lastmod'] = newest_lastmod
    self.lastmod_source_file = newest_source_file
    self.lastmod_source_value = newest_lastmod

  def generate_xml(self):
    """Generate XML sitemap"""
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    for url_data in self.urls:
      url_elem = ET.SubElement(urlset, 'url')
      loc_elem = ET.SubElement(url_elem, 'loc')
      loc_elem.text = url_data['loc']
      lastmod_elem = ET.SubElement(url_elem, 'lastmod')
      lastmod_elem.text = url_data['lastmod']
      changefreq_elem = ET.SubElement(url_elem, 'changefreq')
      changefreq_elem.text = url_data['changefreq']
      priority_elem = ET.SubElement(url_elem, 'priority')
      priority_elem.text = url_data['priority']
    if hasattr(ET, 'indent'):
      ET.indent(urlset, space='  ')
    return urlset

  def save_sitemap(self, filename='sitemap.xml'):
    """Save sitemap to file"""
    self.scan_important_files()
    root = self.generate_xml()
    # Create XML declaration and pretty formatting
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str += ET.tostring(root, encoding='unicode')
    # Save to repository root directory
    sitemap_path = self.repo_path(filename)
    with open(sitemap_path, 'w', encoding='utf-8') as f:
      f.write(xml_str)
    print(f"Sitemap generated: {sitemap_path}")
    print(f"Total URLs: {len(self.urls)}")
    print(f"SITEMAP_LASTMOD={self.lastmod_source_value}")
    print(f"SITEMAP_LASTMOD_SOURCE={self.lastmod_source_file}")
    for url in self.urls:
      print(f"  - {url['loc']} (last modified: {url['lastmod']})")

def main():
  generator = SitemapGenerator()
  generator.save_sitemap()

if __name__ == "__main__":
  main()
