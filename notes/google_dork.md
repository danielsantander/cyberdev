
# Operators

| operator | description |
|----------|-------------|
| Filetype | This operator searches for specific file types. For example, `filetype:pdf` would return PDF files. |
| Inurl | The `inurl:` operator can be used to find specific words within the URL of a page. For example, `inurl:login` would return pages with ‘login’ in the URL. |
| Intext | With the `intext:` operator, you can search for specific text within the content of a web page. For example, `intext:”password”` would yield pages that contain the word “password”. |
| Intitle | The `intitle:` operator is used to search for specific terms in the title of a webpage. For example, `intitle:”index of”` could reveal web servers with directory listing enabled. |
| Link | The `link:` operator can be used to find pages that link to a specific URL. For example, `link:example.com` would find pages linking to example.com. |
| Site | The `site:` operator allows you to search within a specific site. For example, `site:example.com` would search within example.com. |

## Examples

Searching within a specific website: `site:nytimes.com cybersecurity`

Finding specific file types: `filetype:pdf machine learning`

Searching for pages with specific titles: `intitle:"data privacy"`

Finding pages that link to a specific URL: `link:bbc.co.uk/news/technology-57339947`

Search for specific text on a web page: `intext:"cyber threat"`
