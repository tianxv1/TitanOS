import requests
from typing import Dict, Any, Optional


class WebSearchSkill:
    def execute(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
            response = requests.get(url, headers=headers, timeout=10)

            results = []
            if response.status_code == 200:
                results = self._parse_results(response.text, num_results)

            return {
                "query": query,
                "results": results,
                "count": len(results),
                "status": "success"
            }
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "results": [],
                "status": "error"
            }

    def _parse_results(self, html: str, num_results: int) -> list:
        import re
        results = []
        pattern = r'<h3[^>]*>(.*?)</h3>'
        titles = re.findall(pattern, html)[:num_results]

        for i, title in enumerate(titles):
            clean_title = re.sub(r'<[^>]+>', '', title)
            results.append({
                "title": clean_title,
                "url": f"https://www.google.com/search?q=result_{i}"
            })
        return results
