#!/usr/bin/env python3

import os
import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

class SitemapGenerator:
  def __init__(self, base_url="https://kenshikuroki.github.io"):
    self.base_url = base_url
    self.urls = []
    # Set working directory to repository root
    self.repo_root = Path(__file__).parent.parent if __file__ else Path.cwd()
    os.chdir(self.repo_root)

  def add_url(self, loc, lastmod=None, changefreq="monthly", priority="0.5"):
    """Add URL to sitemap"""
    url_data = {
      'loc': f"{self.base_url}{loc}",
      'lastmod': lastmod or datetime.datetime.now().strftime('%Y-%m-%d'),
      'changefreq': changefreq,
      'priority': priority
    }
    self.urls.append(url_data)

  def get_file_modification_date(self, filepath):
    """Get file modification date in YYYY-MM-DD format"""
    if os.path.exists(filepath):
      timestamp = os.path.getmtime(filepath)
      return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    return datetime.datetime.now().strftime('%Y-%m-%d')

  def scan_important_files(self):
    """Scan and add important files to sitemap"""
    # Main page
    index_lastmod = self.get_file_modification_date('index.html')
    self.add_url('/', index_lastmod, 'monthly', '1.0')
    # CV and documents
    cv_path = 'assets/documents/CV_kuroki.pdf'
    if os.path.exists(cv_path):
      cv_lastmod = self.get_file_modification_date(cv_path)
      self.add_url('/assets/documents/CV_kuroki.pdf', cv_lastmod, 'monthly', '0.8')
    # Data files (for SEO if they change frequently)
    data_files = [
      'assets/data/publications.json',
      'assets/data/presentations.json'
    ]
    for data_file in data_files:
      if os.path.exists(data_file):
        lastmod = self.get_file_modification_date(data_file)
        # Don't include JSON files in sitemap as they're not directly accessible
        # But use their modification time to update main page lastmod
        if lastmod > index_lastmod:
          # Update main page lastmod if data is newer
          self.urls[0]['lastmod'] = lastmod

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
    return urlset

  def save_sitemap(self, filename='sitemap.xml'):
    """Save sitemap to file"""
    self.scan_important_files()
    root = self.generate_xml()
    # Create XML declaration and pretty formatting
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str += ET.tostring(root, encoding='unicode')
    # Basic pretty formatting
    xml_str = xml_str.replace('><', '>\n<')
    xml_str = xml_str.replace('<url>', '  <url>')
    xml_str = xml_str.replace('</url>', '  </url>')
    xml_str = xml_str.replace('<loc>', '    <loc>')
    xml_str = xml_str.replace('<lastmod>', '    <lastmod>')
    xml_str = xml_str.replace('<changefreq>', '    <changefreq>')
    xml_str = xml_str.replace('<priority>', '    <priority>')
    # Save to repository root directory
    repo_root = Path(__file__).parent.parent
    sitemap_path = repo_root / filename
    with open(sitemap_path, 'w', encoding='utf-8') as f:
      f.write(xml_str)
    print(f"Sitemap generated: {sitemap_path}")
    print(f"Total URLs: {len(self.urls)}")
    for url in self.urls:
      print(f"  - {url['loc']} (last modified: {url['lastmod']})")

def main():
  generator = SitemapGenerator()
  generator.save_sitemap()

if __name__ == "__main__":
  main()
