## Step 4: Parse HTML Content with Beautiful Soup
Once we have the HTML content of the website, we can use Beautiful Soup to parse it and extract the information we need. We'll create a Beautiful Soup object, which we can then use to navigate the HTML content and extract the tags we're interested in.

```python
soup = BeautifulSoup(response.content, "html.parser")
```



## Step 4: Parse HTML Content with Beautiful Soup
Once we have the HTML content of the website, we can use Beautiful Soup to parse it and extract the information we need. We'll create a Beautiful Soup object, which we can then use to navigate the HTML content and extract the tags we're interested in.

```python
soup = BeautifulSoup(response.content, "html.parser")
```