
# Operators

| operator | description | example|
|----------|--------------------------------------------------|------------------------------------------------------------------------------|
| site     | search within a specific site.                   | `site:example.com` would search within example.com                           |
| filetype | search for specific file types.                  | `filetype:pdf` returns PDF files                                             |
| inurl    | find specific words within the URL of a page.    | `inurl:login` returns pages with ‘login’ in the URL                          |
| intext   | search for text within the content of a web page | `intext:”password”` return pages containing the word “password”              |
| intitle  | search for terms in the title of a webpage       | `intitle:”index of”` could reveal web servers with directory listing enabled |
| link     | find pages that link to a specific URL           | `link:example.com` would find pages linking to example.com                   |

## Examples

Searching within a specific website: `site:nytimes.com cybersecurity`

Finding specific file types: `filetype:pdf machine learning`

Searching for pages with specific titles: `intitle:"data privacy"`

Finding pages that link to a specific URL: `link:bbc.co.uk/news/technology-57339947`

Search for specific text on a web page: `intext:"cyber threat"`

Others:

- `intitle:"webcamXP 5"`
- `allintext:username`
- `allintext:username filetype:log`
