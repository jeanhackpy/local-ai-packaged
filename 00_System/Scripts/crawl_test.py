# Placeholder for crawl_test.py
# Please replace this with your actual script that saves hackernews.md

import asyncio
from crawl4ai import WebCrawler

async def main():
    """
    Crawls Hacker News and saves the content to a markdown file.
    """
    crawler = WebCrawler()
    result = await crawler.run("https://news.ycombinator.com")
    if result and result.markdown:
        with open("hackernews.md", "w", encoding="utf-8") as f:
            f.write(result.markdown)
        print("Successfully crawled Hacker News and saved to hackernews.md")
    else:
        print("Failed to crawl Hacker News.")

if __name__ == "__main__":
    asyncio.run(main())
