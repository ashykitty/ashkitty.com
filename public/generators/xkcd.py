def generate( page, request):
    path = request.path[1:].split("/")
        
    if len(path) == 2:
        if path[1].isnumeric():
            return xkcd( page, path[1])

    return None

def xkcd( page, page_num):
    page_num = int(page_num)
    per_page = 16
    
    with open("data/xkcd2.txt") as file:
        links = file.read().split("\n")[:-1]
        
    total_pages = len(links) // per_page

    if page_num < 0 or page_num > total_pages:
        return None
       
    links = list(reversed(links))
    links = links[page_num*per_page:page_num*per_page+per_page]

    with open("templates/xkcd_post.html") as post:
        post = post.read()

    posts = ""

    for link in links:
        title = link.split("/")[-1].split(".")[0]
        title = title.replace("_"," ")
        posts += post.format(TITLE=title,LINK=link)
    
    btn = "<a href=\"/xkcd/{}\"><button>{}</button></a>"

    page = page.format(
        BODY = posts,
        PAGES= f"{page_num}/{total_pages}",
        FIRST= btn.format(0,"&lt&lt") if page_num > 0 else "",
        LAST = btn.format(total_pages if page_num < total_pages else "","&gt&gt"),
        PREV = btn.format(page_num-1,"&lt") if page_num > 0 else "",
        NEXT = btn.format(page_num+1,"&gt") if page_num < total_pages else "",
        PAGE = f"{page_num}"
    )

    return page 
