from subprocess import Popen, PIPE
import requests
import webbrowser
# this is a wrapper script


def execute_return(cmd):
    # This method will split the result and then return the output and error streams
    args = cmd.split()

    # object insitialize and make two pipe streams
    proc = Popen(args, stdout=PIPE, stderr=PIPE)

    out, err = proc.communicate()  # fetch the output using communicate
    return out, err


def make_req(error):
    # func making calls to SO API to search
    resp = requests.get(
        "https://api.stackexchange.com/"+"2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return resp.json()


def get_urls(json_dict):
    # parsing func and open links
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count += 1
        if count == 3:
            break

    for i in url_list:
        webbrowser.open(i)


if __name__ == "__main__":
    op, err = execute_return("python test.py")
    # decode binary object to string and split and get the last part
    error_message = err.decode("utf-8").strip().split("\r\n")[-1]
    print(error_message)
    print("Searching Stack Overflow...")
    if error_message:
        filter_err = error_message.split(":")

        # json1 = make_req(filter_err[0])
        # json2 = make_req(filter_err[1])
        json3 = make_req(error_message)

        # get_urls(json1)
        # get_urls(json2)
        get_urls(json3)
    else:
        print('No errors, well done')
