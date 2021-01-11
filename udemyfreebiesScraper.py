import requests
import bs4
import json
url = 'https://www.udemyfreebies.com/free-udemy-courses/'
index = 1
scrapped_data = []
while True:
    response = requests.get(url + str(index))
    if response.status_code == 200:
        page = bs4.BeautifulSoup(response.content, "html.parser")
        # gets a list of all the coupons
        coupons = page.select("div[class='coupon-name']")
        if coupons:
            temp = len(scrapped_data)
            for coupon_name in coupons:
                coupon = {}
                coupon_container = coupon_name.parent
                # populate coupon data
                name = coupon_container.select(".coupon-name")
                if name:
                    coupon.update({"name": name[0].h4.a.text})

                link = coupon_container.select(".coupon-name")
                if link:
                    coupon.update({"link": link[0].h4.a["href"]})

                category = coupon_container.select(".coupon-specility")
                if category:
                    coupon.update({"category": category[0].p.text})

                comment = coupon_container.select(".fa-comment")
                if comment:
                    coupon.update({"language": comment[0].parent.text})

                user = coupon_container.select(".fa-user")
                if user:
                    coupon.update({"user": user[0].parent.text})

                star = coupon_container.select(".fa-star")
                if star:
                    coupon.update({"star": star[0].parent.text})

                users = coupon_container.select(".fa-users")
                if users:
                    coupon.update({"users": users[0].parent.text})

                money = coupon_container.select(".fa-money")
                if money:
                    coupon.update({"money": money[0].parent.text})

                scrapped_data.append(coupon)
        print(f'SCRAPED PAGE {index}, FOUND: {len(scrapped_data) - temp}, TOTAL: {len(scrapped_data)}')
        # checks if last page
        if not page.select("ul.theme-pagination")[-1].find_all("a")[-1].text == "»":
            break
        else:
            index += 1
    else:
        break

# write results to html table
style = "<style>table {border: 1px solid black; border-collapse: collapse}</style>"
start = f'<html><head><title>Udemy Coupons</title></head><body>{style}<table style="width:100%">\n'
table_headers = "<tr>"

for head in scrapped_data[0].keys():
    if not head == "link":
        table_headers += f"<th>{head}</th>"
table_headers += "</tr>\n"
end = "</table></body></html>\n"

with open("UdemyCoupons.json", "w", encoding="utf-8") as f:
    json.dump(scrapped_data, f)
# with open("UdemyCouponsNoFree.html", "w", encoding="utf-8") as f:
#     f.write(start)
#     f.write(table_headers)
#     for index, data in enumerate(scrapped_data):
#         if index % 2 == 1:
#             f.write('<tr style="background-color: Cornsilk">\n')
#         else:
#             f.write('<tr style="background-color: Bisque">\n')
#         f.write(f'\t<td><a href="{data.get("link")}">' + f'{data.get("name")}</a></td>\n')
#         keys = list(data.keys())[2:]
#         for key in keys:
#             info = data.get(key)
#             if info:
#                 if len(info) < 43:
#                     f.write(f'\t<td>{info}</td>\n')
#                 else:
#                     f.write(f'\t<td>{info[:43]}...</td>\n')
#             else:
#                 f.write('\t<td style="background-color: red"></td>\n')
#         f.write("</tr>\n")
#     f.write(end)
