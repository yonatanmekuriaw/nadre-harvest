import xml.etree.ElementTree as ET
import cgi, time
import xml.etree.cElementTree as ET
import os
import datetime
import logging
import json

path = "/home/yonathan/Downloads/1/"
communityname = ""
affiliation = ""
for k in range(1, len(os.listdir(path)) + 1):
    path1 = path + str(k)
    array = []
    for i in range(1, len(os.listdir(path1)) + 1):
        for filename in os.listdir(path1 + "/" + str(i)):
            if filename.endswith('.pdf'):
                print(filename)
                fullname = os.path.join(path1 + "/" + str(i), "dublin_core.xml")
                opentree = ET.parse(fullname)
                openroot = opentree.getroot()
                json_data = {}
                title = ""
                authorname = ""
                affiliation = ""
                description = ""
                partof_pages = ""
                upload_type = "publication"
                publication_type = ""
                access_right = ""
                identifier = ""
                imprint_isbn = ""
                imprint_place = ""
                license = "cc-by"
                publicationdate = ""
                related_identifiers = ""
                uri = ""
                id = ""

                doi = os.popen('python doi-generator.py').read()
                print(doi)
                for child in openroot:
                    if child.get("qualifier") == "issued":
                        publicationdate = child.text
                        # print(publicationdate+"-01")
                    elif child.get("qualifier") == "author":
                        authorname = child.text
                        print(authorname)
                    elif child.get("element") == "title":
                        title = child.text
                        # print(title)
                    elif child.get("qualifier") == "abstract":
                        description = child.text
                        # print(description)
                    elif child.get("element") == "publisher":
                        affiliation = child.text
                    elif child.get("element") == "type":
                        publication_type = child.text
                    elif child.get("qualifier") == "uri":
                        uri = child.text


                json_data["metadata"] = {}
                json_data["metadata"]["title"] = title
                json_data["metadata"]["description"] = description
                json_data["metadata"]["creators"] = [{}]
                json_data["metadata"]["creators"][0]["affiliation"] = affiliation
                json_data["metadata"]["creators"][0]["name"] = authorname
                json_data["metadata"]["doi"] = doi
                json_data["metadata"]["partof_pages"] = ""
                json_data["metadata"]["upload_type"] = upload_type
                json_data["metadata"]["publication_type"] = publication_type.lower()
                json_data["metadata"]["access_right"] = "open"
                json_data["metadata"]["communities"] = [{}]
                json_data["metadata"]["communities"][0]["identifier"] = communityname
                json_data["metadata"]["imprint_isbn"] = ""
                json_data["metadata"]["imprint_place"] = ""
                json_data["metadata"]["license"] = {}
                json_data["metadata"]["license"]["id"] = license
                json_data["metadata"]["publication_date"] = publicationdate+"-01"
                json_data["metadata"]["related_identifiers"] = [{}]
                json_data["metadata"]["related_identifiers"][0]["identifier"] = "978-963-313-151-0"
                json_data["metadata"]["related_identifiers"][0]["relation"] = "isPartOf"
                json_data["metadata"]["related_identifiers"][0]["scheme"] = "isbn"
                # reversed_doi = reversed(doi)
                id = doi.split("/")[2]
                print("id-"+id)
                open_json_file = open(os.path.join("", "dspace-metadata/") + id + ".json", 'w')
                write_json = open_json_file.write(json.dumps(json_data))
                logging.info('Json file Ready for upload')
                open_json_file.close()



