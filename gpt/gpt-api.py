import styx_secrets
import requests
import os
from openai import OpenAI
import json
from gpt_secrets import encrypted_bing_api_key, open_api_key


decrypted_bing_api_key = styx_secrets.decrypt(encrypted_bing_api_key).decode("ascii")

headers = {"Ocp-Apim-Subscription-Key": decrypted_bing_api_key}


def get_text(term):
    params = {"q": f"{term} bluetooth", "count": 10, "safeSearch": "Strict"}
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    all_snippets = "\n".join([page['snippet'] for page in search_results['webPages']['value']])
    return all_snippets


os.environ['OPENAI_API_KEY'] = open_api_key

client = OpenAI()


def get_gpt_output(text):
    return client.chat.completions.create(
        # model="gpt-4",
        model="gpt-4-1106-preview",
        # model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": """Read the lines below and detect the type of bluetooth accessory being referred. The type of the bluetooth accessory could be either "headphones", or "speaker", or "wearable", or "car". For all other types, set it to "unknown". Respond in JSON containing type of the bluetooth accessory and the confidence in the classification. Also, include the company and the model of the accessory at lower granularity."""},
            {"role": "user", "content": text}
        ]
    )

##

names_dict = {
    "top-10-regex-absent-ml-unknown": [
        "9.0 bt",
        "fresh ‘n rebel 1arb500",
        "music sound swag",
        "kk-bt01",
        "va370",
        "bls-b21",
        "hy-8898",
        "soundcore a1",
        "b35",
        "skdy barrel"
    ],
    "top-10-regex-absent-ml-other": [
        "ola scooter_music",
        "vhm-314",
        "bt-ss1",
        "mg",
        "miiiw-tw04",
        "zh-android",
        "a60pro",
        "apex-6605",
        "gj_d09btr",
        "autostar"
    ],
    "top-10-regex-absent-ml-small-name": [
        "go3",
        "e1",
        "r8",
        "md",
        "m28",
        "t60",
        "q1",
        "s29",
        "m5",
        "t09"
    ],
    "top-10-regex-mismatch": [
        "mychevrolet",
        "mb bluetooth",
        "bluetooth",
        "f9",
        "caraccessorysystem",
        "my radio",
        "bluetooth music",
        "my rogue",
        "anker soundcore",
        "bt_radio"
    ],
    "top-10-regex-ml-match": [
        "airpods",
        "car multimedia",
        "handsfreelink",
        "uconnect",
        "mazda",
        "my car",
        "apple watch",
        "tws",
        "kia motors",
        "jbl flip 5"
    ],
    "bottom-10-regex-absent-ml-unknown": [
        "m2-531",
        "21 cat radio",
        "hl-boc3361",
        "mountainair-01",
        "dinex d-400",
        "sc1s v2.1",
        "mv-8888",
        "87.5",
        "homewerks(jc243)",
        "navistar radio (98)"
    ],
    "bottom-10-regex-absent-ml-other": [
        "comed",
        "tx-9826",
        "a1-31",
        "sz-1088",
        "imd-6305i",
        "ts-1703",
        "navistar radio (df)",
        "sw-rs02",
        "s6a-l",
        "cql1598-b"
    ],
    "bottom-10-regex-absent-ml-small-name": [
        "bmt",
        "tey",
        "gry",
        "yao",
        "e93",
        "콩콩이",
        "35i",
        "fd6",
        "faw",
        "ive"
    ],
    "bottom-10-regex-mismatch": [
        "rene's buds2",
        "cocos car",
        "yağız adlı kişiye ait buds2",
        "nina car",
        "caitlyns car",
        "squad car",
        "ernesto's buds2",
        "t202-5 speaker",
        "k-0875 speaker",
        "callum’s car"
    ],
    "bottom-10-regex-ml-match": [
        "my car🏎",
        "lindseys car",
        "my car♥️",
        "mark car",
        "victoria's car",
        "des car",
        "bt-car_",
        "devins car",
        "biancas car",
        "staceys car"
    ],
    "recent-overrides": [
        # headphones
        "J90", "J90 Pro", "Bose QC Ultra Headphones", "V7", "J55", "9S", "809",
        "P30", "MOTIF II A.N.C.", "d001", "cacaushow", "a90 pro", "g9s", "m19",
        "n35", "联想thinkplus-th30", "billboard soul track", "y60", "lcdlc pro",
        "联想thinkplus-lp40pro", "h66", "i13", "mod", "j52", "t33", "scorpio",
        "j53", "j18", "pro5", "t59", "q13", "p9", "kd-771",
        "soundcore life q35", "m6", "sony", "c1",
        # speaker
        "c15", "km executive",
        # car
        "Jensen Media Player", "WRX", "T65", "BT21M",
        "Dual Media Player", "MY KICKS", "mykicks", "mykicks laura", "VM-216",
        "VM-216 JOE", "VolvoTrucks", "bc61", "My BT21M", "bc61",
        # wearable
        "RB Stories 00VH", "RB Meta 0081",
        # unknown
        "m6", "s19", "a18", "logitech bt adapter", "localhost", "s23", "bt16",
        "a66", "b01", "c1", "dual media player", "MY KICKS", "VM-216", "bt21m"
    ]
}


if __name__ == "__main__":
    for reason in names_dict:
        with open(f"/Users/amitr/Documents/tmp/accessory_gpt_output/{reason}", 'w', buffering=1) as f:
            for accessory_name in names_dict[reason]:
                try:
                    text_for_accessory = get_text(accessory_name)
                    gpt_output = get_gpt_output(text_for_accessory).choices[0].message.content
                    print(gpt_output)
                    gpt_output_cleaned = gpt_output.replace("```json", "").replace("```", "").replace("type of bluetooth accessory", "llm_type")
                    dict_classification = {"name": accessory_name, "reason": reason}
                    gpt_output_dict = json.loads(gpt_output_cleaned)
                    if type(gpt_output_dict) == list:
                        for output in gpt_output_dict:
                            dict_classification.update(output)
                            print(json.dumps(dict_classification))
                            f.write(json.dumps(dict_classification))
                            f.write("\n")
                    else:
                        dict_classification.update(gpt_output_dict)
                        print(json.dumps(dict_classification))
                        f.write(json.dumps(dict_classification))
                        f.write("\n")
                except Exception as e:
                    print(e)
