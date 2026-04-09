#!/usr/bin/env python3
"""
Enhanced INSPIRE-HEP Metadata Updater
INSPIRE-HEPから包括的な論文情報を取得してpublications.jsonを更新します
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Optional, Any

class EnhancedCitationUpdater:
  def __init__(self, json_path="assets/data/publications.json"):
    self.json_path = Path(json_path)
    self.base_url = "https://inspirehep.net/api"

  def extract_arxiv_id(self, arxiv_string: str) -> Optional[str]:
    """arXiv文字列からIDを抽出"""
    patterns = [
      r'(\d{4}\.\d{4,5})',  # 新形式: 2410.01204
      r'([a-z-]+/\d{7})',   # 旧形式: hep-ph/0123456
    ]
    for pattern in patterns:
      match = re.search(pattern, arxiv_string)
      if match:
        return match.group(1)
    return None

  def extract_doi(self, doi_string: str) -> Optional[str]:
    """DOI文字列からDOIを抽出"""
    patterns = [
      r'doi\.org/(.+)',
      r'(10\.\d+/.+)',
    ]
    for pattern in patterns:
      match = re.search(pattern, doi_string)
      if match:
        return match.group(1)
    return None

  def search_paper_comprehensive(self, publication: Dict) -> Optional[Dict]:
    """複数の方法で論文を検索し、包括的な情報を取得"""
    # 1. 既存のINSPIRE-HEP IDがある場合
    if publication.get('inspire_id'):
      result = self.get_paper_by_inspire_id(publication['inspire_id'])
      if result:
        return result
    # 2. arXiv IDで検索
    for link in publication.get('links', []):
      if link.get('type') == 'arxiv':
        arxiv_id = self.extract_arxiv_id(link.get('text', ''))
        if arxiv_id:
          result = self.search_by_arxiv(arxiv_id)
          if result:
            return result
          time.sleep(1)
    # 3. DOIで検索
    for link in publication.get('links', []):
      if link.get('type') == 'doi':
        doi = self.extract_doi(link.get('url', ''))
        if doi:
          result = self.search_by_doi(doi)
          if result:
            return result
          time.sleep(1)
    # 4. タイトルで検索（最後の手段）
    if publication.get('title'):
      result = self.search_by_title(publication['title'])
      if result:
        return result
    return None

  def get_paper_by_inspire_id(self, inspire_id: str) -> Optional[Dict]:
    """INSPIRE-HEP IDで論文情報を取得"""
    try:
      response = requests.get(f"{self.base_url}/literature/{inspire_id}")
      response.raise_for_status()
      data = response.json()
      return self.extract_paper_metadata({'metadata': data['metadata'], 'id': inspire_id})
    except Exception as e:
      print(f"INSPIRE-HEP ID search failed for {inspire_id}: {e}")
    return None

  def search_by_arxiv(self, arxiv_id: str) -> Optional[Dict]:
    """arXiv IDで検索"""
    try:
      response = requests.get(f"{self.base_url}/literature",
                            params={'q': f'eprint:{arxiv_id}', 'size': 1})
      response.raise_for_status()
      data = response.json()
      if data['hits']['total'] > 0:
        return self.extract_paper_metadata(data['hits']['hits'][0])
    except Exception as e:
      print(f"arXiv search failed for {arxiv_id}: {e}")
    return None

  def search_by_doi(self, doi: str) -> Optional[Dict]:
    """DOIで検索"""
    try:
      response = requests.get(f"{self.base_url}/literature",
      params={'q': f'doi:{doi}', 'size': 1})
      response.raise_for_status()
      data = response.json()
      if data['hits']['total'] > 0:
        return self.extract_paper_metadata(data['hits']['hits'][0])
    except Exception as e:
      print(f"DOI search failed for {doi}: {e}")
    return None

  def search_by_title(self, title: str) -> Optional[Dict]:
    """タイトルで検索（部分一致）"""
    try:
      # タイトルをクリーンアップ
      clean_title = re.sub(r'[^\w\s]', ' ', title).strip()
      query_title = ' '.join(clean_title.split()[:5])  # 最初の5単語を使用
      response = requests.get(f"{self.base_url}/literature",
      params={'q': f'title:"{query_title}"', 'size': 5})
      response.raise_for_status()
      data = response.json()
      # タイトルの類似度をチェック
      for hit in data['hits']['hits']:
        inspire_title = hit['metadata'].get('titles', [{}])[0].get('title', '')
        if self.title_similarity(title, inspire_title) > 0.8:
          return self.extract_paper_metadata(hit)
    except Exception as e:
      print(f"Title search failed for '{title}': {e}")
    return None

  def extract_paper_metadata(self, hit: Dict) -> Dict:
    """INSPIRE-HEP APIレスポンスから必要な情報を抽出"""
    metadata = hit['metadata']
    result = {
      'inspire_id': str(hit['id']),
      'citations': metadata.get('citation_count', 0),
      'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    # タイトル
    titles = metadata.get('titles', [])
    if titles:
      result['title'] = titles[0].get('title', '')
    # 著者リスト
    authors = metadata.get('authors', [])
    if authors:
      author_names = []
      for author in authors:
        full_name = author.get('full_name', '')
        if full_name:
          author_names.append(full_name)
      result['authors'] = ', '.join(author_names)
    # 出版情報
    pub_info = metadata.get('publication_info', [])
    if pub_info:
      pub = pub_info[0]
      result['journal'] = pub.get('journal_title', '')
      result['volume'] = pub.get('journal_volume', '')
      if pub.get('page_start') and pub.get('page_end'):
        result['pages'] = f"pub.get('page_start')-pub.get('page_end')"
      elif pub.get('page_start'):
        result['pages'] = pub.get('page_start')
      elif pub.get('artid'):
        result['pages'] = pub.get('artid')
      result['year'] = pub.get('year', '')
    # 出版年（代替）
    if not result.get('year'):
      preprint_date = metadata.get('preprint_date', '')
      if preprint_date:
        result['year'] = preprint_date[:4]
    # arXiv情報
    arxiv_eprints = metadata.get('arxiv_eprints', [])
    if arxiv_eprints:
      result['arxiv_id'] = arxiv_eprints[0].get('value', '')
      result['arxiv_categories'] = arxiv_eprints[0].get('categories', [])
    # DOI
    dois = metadata.get('dois', [])
    if dois:
      result['doi'] = dois[0].get('value', '')
    # URLs
    urls = metadata.get('urls', [])
    result['urls'] = []
    for url in urls:
      result['urls'].append({
        'description': url.get('description', ''),
        'value': url.get('value', '')
      })
    return result

  def title_similarity(self, title1: str, title2: str) -> float:
    """簡単なタイトル類似度計算"""
    # 単語レベルでの類似度（Jaccard係数）
    words1 = set(re.findall(r'\w+', title1.lower()))
    words2 = set(re.findall(r'\w+', title2.lower()))
    if not words1 or not words2:
      return 0.0
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    return intersection / union if union > 0 else 0.0

  def merge_metadata(self, current_pub: Dict, inspire_data: Dict) -> Dict:
    """現在の出版物データとINSPIRE-HEP データをマージ"""
    updated_pub = current_pub.copy()
    # 常に更新する項目（last_updatedは変更があった場合のみ更新するためここには含めない）
    always_update = ['citations']
    # 空の場合のみ更新する項目
    update_if_empty = ['title', 'authors', 'inspire_id']
    # リンク情報の更新
    update_links = True
    for key, value in inspire_data.items():
      if key in always_update:
        updated_pub[key] = value
      elif key in update_if_empty and (not updated_pub.get(key) or updated_pub.get(key) == ''):
        updated_pub[key] = value
      elif key == 'categories' and value:
        updated_pub[key] = value
      elif key == 'urls' and value:
        updated_pub[key] = value
    # リンク情報の自動更新
    if update_links:
      updated_pub = self.update_links(updated_pub, inspire_data)
    return updated_pub

  def update_links(self, publication: Dict, inspire_data: Dict) -> Dict:
    """リンク情報を更新"""
    links = publication.get('links', [])
    # DOI リンクの追加/更新
    if inspire_data.get('doi'):
      doi_exists = any(link.get('type') == 'doi' for link in links)
      if not doi_exists:
        links.append({
          'type': 'doi',
          'text': f"{inspire_data['journal']} {inspire_data['volume']}, {inspire_data['pages']} ({inspire_data['year']})",
          'url': f"https://doi.org/{inspire_data['doi']}"
        })
    # arXiv リンクの追加/更新
    if inspire_data.get('arxiv_id'):
      arxiv_exists = any(link.get('type') == 'arxiv' for link in links)
      if not arxiv_exists:
        links.append({
          'type': 'arxiv',
          'text': f"arXiv:{inspire_data['arxiv_id']}",
          'url': f"https://arxiv.org/abs/{inspire_data['arxiv_id']}"
        })
    publication['links'] = links
    return publication

  def update_publications(self, backup=True) -> bool:
    """publications.jsonを更新"""
    if not self.json_path.exists():
      print(f"File not found: {self.json_path}")
      return False
    # JSONファイルを読み込み
    try:
      with open(self.json_path, 'r', encoding='utf-8') as f:
        publications = json.load(f)
    except Exception as e:
      print(f"Failed to read JSON file: {e}")
      return False
    print(f"Updating {len(publications)} publications...")
    updated_count = 0
    failed_count = 0
    # 各論文の情報を更新
    for i, pub in enumerate(publications):
      print(f"\n[{i+1}/{len(publications)}] Processing: {pub.get('title', 'Unknown Title')[:60]}...")
      inspire_data = self.search_paper_comprehensive(pub)
      if inspire_data:
        old_citations = pub.get('citations', 0)
        updated_pub = self.merge_metadata(pub, inspire_data)
        # 変更があったかチェック
        changes = []
        if old_citations != updated_pub.get('citations', 0):
          changes.append(f"citations: {old_citations} → {updated_pub['citations']}")
        if pub.get('inspire_id') != updated_pub.get('inspire_id'):
          changes.append(f"inspire_id: {pub.get('inspire_id', 'None')} → {updated_pub['inspire_id']}")
        # その他の変更をチェック
        for key in ['title', 'authors']:
          old_val = pub.get(key, '')
          new_val = updated_pub.get(key, '')
          if old_val != new_val and new_val:
            changes.append(f"{key}: updated")
        if changes:
          updated_pub['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          publications[i] = updated_pub
          print(f"  ✅ Updated: {', '.join(changes)}")
          updated_count += 1
        else:
          print(f"  ℹ️  No changes (citations: {updated_pub.get('citations', 0)})")
      else:
        print(f"  ❌ Could not find INSPIRE-HEP data")
        failed_count += 1
      # API制限対策
      time.sleep(2)
    # 更新されたJSONを保存
    try:
      with open(self.json_path, 'w', encoding='utf-8') as f:
        json.dump(publications, f, indent=2, ensure_ascii=False)
      print(f"\n" + "="*50)
      print(f"✅ Update completed!")
      print(f"📊 Updated: {updated_count} publications")
      print(f"❌ Failed: {failed_count} publications")
      print(f"📄 File saved: {self.json_path}")
      print(f"CITATION_UPDATED_COUNT={updated_count}")
      return True
    except Exception as e:
      print(f"Failed to save JSON file: {e}")
      return False

  def generate_report(self) -> Dict:
    """更新レポートを生成"""
    if not self.json_path.exists():
      return {}
    try:
      with open(self.json_path, 'r', encoding='utf-8') as f:
        publications = json.load(f)
      total_citations = sum(pub.get('citations', 0) for pub in publications)
      with_inspire_id = sum(1 for pub in publications if pub.get('inspire_id'))
      categories = {}
      for pub in publications:
        for cat in pub.get('categories', []):
          categories[cat] = categories.get(cat, 0) + 1
      return {
        'total_publications': len(publications),
        'total_citations': total_citations,
        'with_inspire_id': with_inspire_id,
        'coverage': f"{with_inspire_id/len(publications)*100:.1f}%",
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      }
    except Exception as e:
      print(f"Report generation failed: {e}")
      return {}

def main():
  print("Enhanced INSPIRE-HEP Metadata Updater")
  print("=" * 50)
  updater = EnhancedCitationUpdater()
  # 更新前のレポート
  print("Current status:")
  report = updater.generate_report()
  for key, value in report.items():
    print(f"  {key}: {value}")
  print("\nStarting update...")
  success = updater.update_publications()
  if success:
    print("\n🎉 Update completed successfully!")
    # 更新後のレポート
    print("\nUpdated status:")
    new_report = updater.generate_report()
    for key, value in new_report.items():
      print(f"  {key}: {value}")
  else:
    print("\n❌ Update failed. Please check the error messages above.")

if __name__ == "__main__":
  main()
