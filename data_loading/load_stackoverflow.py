import pandas as pd
import xml.etree.ElementTree as ET
import csv
import gc

# 58000000

tree = ET.iterparse('F:/posts/Posts.xml')
tree = iter(tree)

with open('F:/posts/Posts.csv', 'w', newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Id", "PostTypeId", "ParentId", "CreationDate", "Score", "Body", "OwnerUserId", "OwnerDisplayName", "LastEditorUserId", "LastEditDate", "LastActivityDate", "CommentCount", "ContentLicense", "AcceptedAnswerId", "ViewCount", "Title", "Tags", "AnswerCount", "LastEditorDisplayName", "FavoriteCount", "CommunityOwnedDate", "ClosedDate"]
    )
    writer.writeheader()
    i = 0
    for element in tree:
        writer.writerow(element[1].attrib)
        element[1].clear()
        i += 1
        if i % 1000000 == 0:
            print(i / 58000000 * 100, "%", end="\r")
