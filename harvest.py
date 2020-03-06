import zenodio.harvest
from urllib.request import urlopen
import json
import urllib.request
import os
import logging

community_title = "nadre"
collection = zenodio.harvest.harvest_collection(community_title)

for record in collection.records():
    # print(record.doi)
    id = ''
    url = ''
    pdf_file = ''
    count = 0
    json_data = {}
    for doid in reversed(record.doi):
        if doid == "/":
            print(id[-1::-1])
            url = "https://nadre.ethernet.edu.et/api/records/" + id[-1::-1]
            # print(url)
            json_file = urlopen(url)
            read_json = json.loads(json_file.read())
            if "files" not in read_json:
                print("There is no pdf file provided or file is corrupted with DOI: " + doid)
            else:
                pdf_file = read_json['files'][0]['links']['self']
                print(pdf_file)
                urllib.request.urlretrieve(pdf_file, os.path.join("", "metadata/") + id[-1::-1] + ".pdf")

                json_data["metadata"] = {}
                json_data["metadata"]["title"] = read_json["metadata"]['title']
                json_data["metadata"]["description"] = read_json["metadata"]['description']
                json_data["metadata"]["creators"] = [{}]
                if "affiliation" not in read_json["metadata"]:
                    print("No affiliation provided")
                else:
                    json_data["metadata"]["creators"][0]["affiliation"] = read_json["metadata"]["creators"][0]["affiliation"]
                json_data["metadata"]["creators"][0]["name"] = read_json["metadata"]["creators"][0]["name"]
                json_data["metadata"]["doi"] = read_json["doi"]
                json_data["metadata"]["partof_pages"] = ""
                # json_data["metadata"]["keywords"] = [""] * len(read_json["metadata"]["keywords"])
                # if "keywords" not in read_json["metadata"]:
                #     print("No keyword provided")
                # else:
                #     for m in range(0, len(read_json["metadata"]["keywords"]) - 1):
                #         json_data["metadata"]["keywords"][m] = read_json["metadata"]["keywords"][m]
                json_data["metadata"]["upload_type"] = read_json["metadata"]["resource_type"]["type"]
                if "subtype" not in read_json["metadata"]:
                    json_data["metadata"]["publication_type"] = "thesis"
                else:
                    json_data["metadata"]["publication_type"] = read_json["metadata"]["resource_type"]["subtype"]
                json_data["metadata"]["access_right"] = read_json["metadata"]["access_right"]
                # json_data["metadata"]["communities"] = []
                json_data["metadata"]["communities"] = [{}]
                # for i in range(0, len(read_json["metadata"]["communities"]) - 1):
                # json_data["metadata"]["communities"][0]["identifier"] = community_title
                json_data["metadata"]["communities"][0]["identifier"] = "zenodo"

                print("communties----" + str(len(read_json["metadata"]["communities"])))

                # if "communities" not in read_json["metadata"]:
                #     print("No community provided")
                # else:
                #     json_data["metadata"]["communities"][0]["identifier"] = read_json["metadata"]["communities"][0]["id"]
                # communities = []
                # communities_name = {}
                # c2 = []
                # for i in range(len(read_json["metadata"]["communities"])):
                #    print(read_json["metadata"]["communities"][i]["id"])
                #    communities.append(read_json["metadata"]["communities"][i]["id"])
                #    communities_name["identifier"] = read_json["metadata"]["communities"][i]["id"]
                #    print(communities)
                #    for j in range(len(communities)-1):
                #        communities_name["identifier"] = ""
                       # json_data["metadata"]["communities"][j]["identifier"] = communities[j]

                   # c2.append(communities_name)
                   # for m in communities:
                   #     json_data["metadata"]["communities"]["identifier"] = m
                   # print(c2)
                   # json_data["metadata"]["communities"].append(communities_name)

                   # if len(read_json["metadata"]["communities"]) ==
                   # json_data["metadata"]["communities"][i]["identifier"] = communities[i]
                   # json_data["metadata"]["communities"][1]["identifier"] = communities[1]
                # m = [0,1,2,3]
                # for i in m:
                #     if i == (len(read_json["metadata"]["communities"])-1):
                #
                json_data["metadata"]["imprint_isbn"] = ""
                json_data["metadata"]["imprint_place"] = ""
                json_data["metadata"]["license"] = read_json["metadata"]["license"]
                json_data["metadata"]["publication_date"] = read_json["metadata"]["publication_date"]
                json_data["metadata"]["related_identifiers"] = [{}]
                json_data["metadata"]["related_identifiers"][0]["identifier"] = "978-963-313-151-0"
                json_data["metadata"]["related_identifiers"][0]["relation"] = "isPartOf"
                json_data["metadata"]["related_identifiers"][0]["scheme"] = "isbn"

                open_json_file = open(os.path.join("", "metadata/") + id[-1::-1] + ".json", 'w')
                write_json = open_json_file.write(json.dumps(json_data))
                logging.info('Json file Ready for upload')
                open_json_file.close()
                # print(read_json)
            break
        id += doid
