from google.cloud import bigquery
import json

from gpt_secrets import bq_table

# Construct a BigQuery client object.
client = bigquery.Client()

table_id = bq_table


names_set = {
    "top-10-regex-absent-ml-unknown",
    "top-10-regex-absent-ml-other",
    "top-10-regex-absent-ml-small-name",
    "top-10-regex-mismatch",
    "top-10-regex-ml-match",
    "bottom-10-regex-absent-ml-unknown",
    "bottom-10-regex-absent-ml-other",
    "bottom-10-regex-absent-ml-small-name",
    "bottom-10-regex-mismatch",
    "bottom-10-regex-ml-match",
    "recent-overrides"
}


if __name__ == "__main__":
    for name in names_set:
        with open(f"/Users/amitr/Documents/tmp/accessory_gpt_output/{name}", "r") as f:
            lines = f.readlines()
            line_dict_list = []
            for line in lines:
                line_dict = json.loads(line)
                # a couple of accessories have "accessories" and "accessoryN", ignoring them
                if "accessories" in line_dict or "accessory1" in line_dict:
                    continue
                line_dict["type"] = str(line_dict.get("type", line_dict.get("accessory_type")))
                if "accessory_type" in line_dict:
                    del line_dict["accessory_type"]
                line_dict["company"] = str(line_dict.get("company", ""))
                line_dict["model"] = str(line_dict.get("model", ""))
                print(line_dict)
                line_dict_list.append(line_dict)
            errors = client.insert_rows_json(table_id, line_dict_list)  # Make an API request.
            if not errors:
                print("New rows have been added. {}".format(line_dict_list))
                print("Success! :)")
            else:
                print("Encountered errors while inserting rows: {}".format(errors))
                print("Failure :(")


