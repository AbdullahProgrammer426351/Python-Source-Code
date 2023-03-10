import multiprocessing
import requests
import concurrent.futures
#mutli-processing is a technnigue to execute heavy tasks on multiple cpu's parallelly
def downloadFile(url, name):
    print(f"Started Downloading {name}")
    response = requests.get(url)
    open(f"images/image{name}.jpg", "wb").write(response.content)
    print(f"Finished Downloading {name}")

if __name__ == "__main__":
    url = "https://picsum.photos/3000/1500"


    # if we not require loop variable then we can throw '_' instead of i or some other variable
    # for _ in range(5):
    # pros = []
    # for i in range(5):
    #     # downloadFile(url, i)
    #     p = multiprocessing.Process(target=downloadFile, args=[url, i])
    #     p.start()
    #     pros.append(p)


    # for p in pros:
    #     p.join()

    with concurrent.futures.ProcessPoolExecutor() as exeutor:
        l1 = [url for i in range(10)]
        l2 = [i for i in range(10)]
        results = exeutor.map(downloadFile, l1, l2)
        for r in results:
            print(r)