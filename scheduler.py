import os,requests,json

access_url = "https://open.welink.huaweicloud.com/api/auth/v2/tickets"
access_body = {
    "client_id": "20230925224247033213466",
    "client_secret": "e81bb0b0-4129-4679-b971-4291303991a9", 
}
access_head = {
    "Content-Type": "application/json"
}

def get_access_code():
    reply = requests.post(access_url,headers=access_head, data=json.dumps(access_body))
    text = reply.text
    jobj = json.loads(text)
    if jobj['code'] == "0" :
        # Accept
        acctoken = jobj['access_token']
        # Save
        with open('./saved/access_token.txt','w') as f:
            f.write(acctoken)
            print("saved access_token.txt")
    else:
        print("Error: ",jobj['code'],jobj['message'])


if __name__ == "__main__":
    get_access_code()