import scrapy


class BookSpider(scrapy.Spider):
    name = "books"
    page_count = 0
    bk_count = 1 
    file = open("list_of_books.txt","a",encoding="UTF-8")
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=5&filter_in_stock=1"

    ]
    def parse(self, response):
        book_names = response.css("div.name.ellipsis a span::text").extract()
        book_authors = response.css("div.author span a span::text").extract()
        book_publishers = response.css("div.publisher span a span::text").extract()
        i = 0
        while(i<len(book_publishers)):
            """yield{
                "name" :book_names[i],
                "author":book_authors[i],
                "publisher":book_publishers[i]
            }"""
            self.file.write("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
            self.file.write("en çok satanlar listemizdeki "+ str(self.bk_count) + ". sırada bulunan sanat eserimiz =\n")
            self.file.write("Kitap İsmi : " + book_names[i] +"\n")
            self.file.write("Yazar Bilgisi : " + book_authors[i] +"\n")
            self.file.write("Yayınevi Bilgisi : " +book_publishers[i] +"\n")
            self.file.write("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
            self.bk_count += 1
            i += 1
        next_url = response.css("a.next::attr(href)").extract_first()
        self.page_count += 1

        if next_url is  not None and self.page_count != 10:
            yield scrapy.Request(url= next_url,callback=self.parse)
        else:
            self.file.close()