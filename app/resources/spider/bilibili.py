UP_STRING_EXEC_STATEMENTS = """
up = {
    "name": up_name,
    "up_id": up_id,
    "follow_number": follow_number,
    "fans_number": fans_number,
    "total_contributions_number": total_contributions_number,
    "contribution": {
        "video": [],
        "audio": [],
        "article": [],
        "album": []
    }
}
"""

UP_EXEC_STATEMENTS = """
up_name_node = driver.get_node_or_nodes(driver=driver, find_mode="id", param="h-name")
up_name = driver.get_node_value(up_name_node, text=True)
navigator_node = driver.get_node_or_nodes(driver=driver, find_mode="id", param="navigator")
follow_number_node = driver.get_node_or_nodes(driver=navigator_node, find_mode="class_name", param="n-gz")
follow_number = driver.get_node_value(follow_number_node, attribute="title")
fans_number_node = driver.get_node_or_nodes(driver=navigator_node, find_mode="class_name", param="n-fs")
fans_number = driver.get_node_value(fans_number_node, attribute="title")
total_contributions_number_node = driver.get_node_or_nodes(driver=navigator_node, find_mode="class_name", param="n-num")
total_contributions_number = driver.get_node_value(total_contributions_number_node, text=True)
"""

UPDATE_UP_EXEC_STATEMENTS = {
    "video":
        """
video_categories = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div#submit-video-type-filter > a", multi=True)
for video_category in video_categories:
    number_node = driver.get_node_or_nodes(driver=video_category, find_mode="tag_name", param="span")
    number = driver.get_node_value(number_node, text=True)
    
    name = driver.get_node_value(video_category, text=True).replace(number, "")
    type_dict = {"type": name, "number": number}
    update_list.append(type_dict)
        """,
    "audio":
        """
page_audio_node = driver.get_node_or_nodes(driver=driver, find_mode="id", param="page-audio")
cur_li_node = driver.get_node_or_nodes(driver=page_audio_node, find_mode="class_name", param="cur")
cur_li = driver.get_node_value(cur_li_node, text=True, regular=True, regular_pattern=driver.number_regular)
type_dict = {"type": "全部", "number": cur_li}
update_list.append(type_dict)
        """,
    "article":
        """
page_article_node = driver.get_node_or_nodes(driver=driver, find_mode="id", param="page-article")
cur_li_node = driver.get_node_or_nodes(driver=page_article_node, find_mode="class_name", param="cur")
cur_li = driver.get_node_value(cur_li_node, text=True, regular=True, regular_pattern=driver.number_regular)
type_dict = {"type": "全部", "number": cur_li}
update_list.append(type_dict)
        """,
    "album":
        """
album_content_node =  driver.find_element_by_id("page-myalbum").find_element_by_class_name("album-content")
album_categories = driver.get_node_or_nodes(driver=album_content_node, find_mode="css_selector", param="div.tab-list > span.tab", multi=True)
for album_category in album_categories:
    name_node = driver.get_node_or_nodes(driver=album_category, find_mode="css_selector", param="span.name")
    name = driver.get_node_value(name_node, text=True)
    
    count_node = driver.get_node_or_nodes(driver=album_category, find_mode="css_selector", param="span.count")
    count = driver.get_node_value(count_node, text=True)
    
    type_dict = {"type": name, "number": count}
    update_list.append(type_dict)
if not update_list:
    update_list.append({"type": "全部", "number": "0"})
        """
}

EXEC_STATEMENTS = {
    "video":
        """
video_list_lis = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div#submit-video-list > ul.cube-list > li > a.title", multi=True)
for video_list_li in video_list_lis:
    href = driver.get_node_value(video_list_li, attribute="href")
    file.write(f"{up_id}-{href}\\n")
next_pager = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div#submit-video-list > ul.be-pager > li.be-pager-next")
next_pager_class = driver.get_node_value(next_pager, attribute="class")
while "be-pager-disabled" not in next_pager_class:
    next_pager.click()
    sleep(1)
    video_list_lis = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div#submit-video-list > ul.cube-list > li > a.title", multi=True)
    for video_list_li in video_list_lis:
        href = driver.get_node_value(video_list_li, attribute="href")
        file.write(f"{up_id}-{href}\\n")
    next_pager = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div#submit-video-list > ul.be-pager > li.be-pager-next")
    next_pager_class = driver.get_node_value(next_pager, attribute="class")
        """,
    "audio":
        """
content_node = driver.find_element_by_id("page-audio").find_element_by_class_name("content")
audio_list_lis = content_node.find_element_by_class_name("clearfix").find_elements_by_tag_name("li")
for audio_list_li in audio_list_lis:
    href = audio_list_li.find_element_by_class_name("cover").get_attribute("href")
    file.write(f"{up_id}-{href}\\n")
next_pager = driver.get_node_or_nodes(driver=content_node, find_mode="class_name", param="be-pager-next")
next_pager_class = driver.get_node_value(next_pager, attribute="class")
while "be-pager-disabled" not in next_pager_class:
    next_pager.click()
    sleep(1)
    content_node = driver.find_element_by_id("page-audio").find_element_by_class_name("content")
    audio_list_lis = content_node.find_element_by_class_name("clearfix").find_elements_by_tag_name("li")
    for audio_list_li in audio_list_lis:
        href = audio_list_li.find_element_by_class_name("cover").get_attribute("href")
        file.write(f"{up_id}-{href}\\n")
    
    next_pager = driver.get_node_or_nodes(driver=content_node, find_mode="class_name", param="be-pager-next")
    next_pager_class = driver.get_node_value(next_pager, attribute="class")
        """,
    "article":
        """
main_content_node = driver.find_element_by_id("page-article").find_element_by_class_name("main-content")
article_list_lis = main_content_node.find_element_by_class_name("content").find_elements_by_class_name("article-item")
for article_list_li in article_list_lis:
    href_node = driver.get_node_or_nodes(driver=article_list_li, find_mode="css_selector", param="h2 > a")
    href = driver.get_node_value(href_node, attribute="href")
    file.write(f"{up_id}-{href}\\n")
next_pager = driver.get_node_or_nodes(driver=main_content_node, find_mode="class_name", param="be-pager-next")
next_pager_class = driver.get_node_value(next_pager, attribute="class")
while "be-pager-disabled" not in next_pager_class:
    next_pager.click()
    sleep(1)
    main_content_node = driver.find_element_by_id("page-article").find_element_by_class_name("main-content")
    article_list_lis = main_content_node.find_element_by_class_name("content").find_elements_by_class_name("article-item")
    for article_list_li in article_list_lis:
        href_node = driver.get_node_or_nodes(driver=article_list_li, find_mode="css_selector", param="h2 > a")
        href = driver.get_node_value(href_node, attribute="href")
        file.write(f"{up_id}-{href}\\n")
    next_pager = driver.get_node_or_nodes(driver=main_content_node, find_mode="class_name", param="be-pager-next")
    next_pager_class = driver.get_node_value(next_pager, attribute="class")
        """,
    "album":
        """
album_lists = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div.album-list > div.album-card > a.title", multi=True)
for album in album_lists:
    href = driver.get_node_value(album, attribute="href")
    file.write(f"{up_id}-{href}\\n")
next_pager = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div.pagination > ul.link-panigation > li", multi=True)[-1]
next_pager_style = driver.get_node_value(next_pager, attribute="style")
while not next_pager_style:
    next_pager.click()
    sleep(1)
    album_lists = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div.album-list > div.album-card > a.title", multi=True)
    for album in album_lists:
        href = driver.get_node_value(album, attribute="href")
        file.write(f"{up_id}-{href}\\n")
    next_pager = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div.pagination > ul.link-panigation > li", multi=True)[-1]
    next_pager_style = driver.get_node_value(next_pager, attribute="style")
        """
}

SINGLE_EXEC_STATEMENTS = {
    "video":
        """
viewbox_report_node = driver.get_node_or_nodes(driver=driver, find_mode="id", param="viewbox_report")
title = driver.get_node_value_by_while(driver=viewbox_report_node, find_mode="tag_name", param="h1", regular=False)
view = driver.get_node_value_by_while(driver=viewbox_report_node, param="view")
dm = driver.get_node_value_by_while(driver=viewbox_report_node, param="dm")
driver.execute_script(driver.js_500)
sleep(3)
ops = driver.find_element_by_id("arc_toolbar_report").find_element_by_class_name("ops")
like = driver.get_node_value_by_while(driver=ops, param="like")
coin = driver.get_node_value_by_while(driver=ops, param="coin")
collect = driver.get_node_value_by_while(driver=ops, param="collect")
share_node = driver.get_node_or_nodes(driver=ops, find_mode="class_name", param="share")
share = driver.get_node_value(share_node, text=True)
driver.execute_script(driver.js_400)
driver.execute_script(driver.js_500)
comment_node = driver.find_element_by_id("comment")
comment = driver.get_node_value_by_while(driver=comment_node, param="b-head", text=True)
single_dict = {
    "up_id": up_id,
    "title": title,
    "view": view,
    "dm": dm,
    "like": like,
    "coin": coin,
    "collect": collect,
    "share": share,
    "comment": comment,
    "url": url
}
        """,
    "audio":
        """
title_node = driver.get_node_or_nodes(driver=driver, find_mode="id", param="song_detail_click_video_entrance") 
title = driver.get_node_value(title_node, attribute="title")
origin_time_node = driver.get_node_or_nodes(driver=driver, find_mode="class_name", param="song-time")
time = driver.get_node_value(origin_time_node, text=True, regular=True, regular_pattern=driver.date_regular)
song_shares = driver.find_element_by_class_name("share-board").find_elements_by_class_name("song-share")
single_dict = {
    "up_id": up_id,
    "url": url,
    "title": title,
    "time": time,
}
for index, song_share in enumerate(song_shares):
    value_node = driver.get_node_or_nodes(driver=song_share, find_mode="tag_name", param="div")
    value = driver.get_node_value(value_node, text=True, regular=True, regular_pattern=driver.number_regular)
    single_dict[driver.index_to_key[str(index)]] = value
print(f"single_dict: {single_dict}")
        """,
    "article":
        """
title_node = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="h1.title")
title = driver.get_node_value(title_node, text=True)

create_time_node = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="span.create-time")
create_time = driver.get_node_value(create_time_node, attribute="data-ts")
sleep(0.5)
article_data_nodes = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div.article-data > span", multi=True)
view, like, comment = driver.get_nodes_value(nodes=article_data_nodes, text=True, regular=True)
ops = driver.find_element_by_class_name("ops")
coin_node = driver.get_node_or_nodes(driver=ops, find_mode="css_selector", param="span.coin-btn > span")
coin = driver.get_node_value(coin_node, text=True)
collect_node = driver.get_node_or_nodes(driver=ops, find_mode="css_selector", param="span.fav-btn > span")
collect = driver.get_node_value(collect_node, text=True)
single_dict = {
    "up_id": up_id,
    "url": url,
    "title": title,
    "create_time": create_time,
    "coin": coin,
    "collect": collect,
    "view": view,
    "like": like,
    "comment": comment
}
print(single_dict)
        """,
    "album":
        """
description = driver.get_node_value_by_while(driver=driver, find_mode="css_selector", param="article.article-content > div.content > div.description", text=True, regular=False)
create_date_node = driver.get_node_or_nodes(driver=driver, find_mode="class_name", param="create-date")
create_date = driver.get_node_value(create_date_node, text=True)[5:]
visit_info_nodes = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div.visit-info > span", multi=True)
view, collect, support = driver.get_nodes_value(visit_info_nodes, text=True, regular=True)
like_node = driver.get_node_or_nodes(driver=driver, find_mode="css_selector", param="div.dashboard > ul > li.like > dl > dt > span.number")
like = driver.get_node_value(like_node, text=True)
single_dict = {
    "up_id": up_id,
    "url": url,
    "description": description,
    "create_date": create_date,
    "view": view,
    "collect": collect,
    "support": support,
    "like": like
}
print(single_dict)
        """
}
