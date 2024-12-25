import json

with open("parsed_html.json", "r", encoding ="utf-8") as outputFile:

        data = json.loads(outputFile.read())
        new_data = list(data.values())
        print(new_data[0])
        total = len(new_data)
        noDate, noDescription, noBoth = 0, 0, 0

        for dic in new_data[0]:
            if dic["description"] == None and dic["published_date"] == None:
                noBoth += 1
            elif dic["description"] == None:
                noDescription += 1
            elif dic["published_date"] == None:
                noDate += 1
        print({"DateFailures": noDate / total, "DescriptionFailures": noDescription / total, "BothFailures": noBoth/total})

        
        