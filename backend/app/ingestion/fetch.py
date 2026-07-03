import httpx
from bs4 import BeautifulSoup


def fetch_statement(date: str) -> str:
    url = f"https://www.federalreserve.gov/newsevents/pressreleases/monetary{date}a.htm"
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_= "col-xs-12 col-sm-8 col-md-8")
    paragraphs = content.find_all("p")
    return "\n\n".join(p.get_text() for p in paragraphs)

if __name__ == "__main__":
    print(fetch_statement("20260617"))