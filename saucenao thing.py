import requests
import os
import pandas as pd
from time import perf_counter, sleep


def get_sauce(path):
    # for every image in the path, get the source
    base_url = r"https://saucenao.com/search.php"
    file_array = []
    source_array = []
    similarity_array = []
    failed_files_array = []
    matched_files_counter = 0

    limit_counter = 0
    limit_start = perf_counter()

    print("{} files inside directory".format(len(os.listdir(path))))

    for file in os.listdir(path):  # for each file
        start = perf_counter()  # start timing
        file_path = os.path.join(path, file)
        with open(file_path, "rb") as f:  # convert file into binary
            files = {"file": f.read()}

        parameters = {
            "api_key": "",
            "file": file_path,
            "url": None,
            "output_type": "2"}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.84 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-DE,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive'}

        # how to settle connection errors #
        try:
            r = requests.post(url=base_url, params=parameters, files=files, headers=headers)
            limit_counter += 1  # only successful connection counts as a request
        except requests.ConnectionError:
            print("Can't seem to connect properly. Going to skip this file {}".format(file))
            failed_files_array.append(file)
            continue

        except Exception as e:
            print("Something went wrong: {}".format(e))
            print("Skipping {}".format(file))
            failed_files_array.append(file)
            continue

        # get my status codes in case something breaks #
        if r.status_code != 200:
            print("Something went wrong: {}".format(r.status_code))
            failed_files_array.append(file)
            continue

        # how to make sure i make only 11 requests in 30 seconds #
        if limit_counter >= 10 and perf_counter() - limit_start < 30:  # too many requests (11 requests/30 seconds)
            sleep_duration = round(30 - perf_counter() + limit_start, 2)
            print("OVER LIMIT, sleeping for {} seconds".format(sleep_duration))
            sleep(sleep_duration)
            limit_counter = 0
            limit_start = perf_counter()

        elif perf_counter() - limit_start > 30 and limit_counter <= 10:  # if past request limit
            limit_start = perf_counter()
            limit_counter = 0

        with open("json.txt", "a", encoding="utf-8") as fjson:  # TESTING PURPOSE
            fjson.write(str(r.json()))
            fjson.write("\n\n\n")

        data = r.json()["results"][0]  # retrieving data from the json received
        source = data["data"]["ext_urls"][0]
        similarity = data["header"]["similarity"]

        file_array.append(file)
        source_array.append(source)
        similarity_array.append(similarity)

        end = perf_counter()
        difference = end - start
        print("{} done, similarity {}%, taking {} seconds".format(file, similarity, round(difference, 2)))
        matched_files_counter += 1

    print("{} files matched. {} files failed.".format(matched_files_counter, len(failed_files_array)))

    if len(failed_files_array) > 0:
        with open("failed_files.txt", "w") as f:
            for failed_file in failed_files_array:
                line = os.path.join(path, failed_file) + "\n"
                f.write(line)
        print("Failed files have been logged")

    df_sources = pd.DataFrame({"file": file_array,
                       "source": source_array,
                       "similarity": similarity_array})
    return df_sources


if __name__ == "__main__":
    df = get_sauce(r"C:\Users\Amp\Desktop\python\Getting image sources\images")
    df.to_csv("df.csv")
