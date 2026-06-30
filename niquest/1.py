# import niquests

# response = niquests.get("https://jsonplaceholder.typicode.com/posts/1")

# print(response.status_code)
# print('#'*30)
# print(response.text)
# print('#'*30)
# print(response)
# print('#'*30)
# print(response.json())
# print('#'*30)
# print(response.json()['userId'])
# print(response.json()['title'])
# print(response.json()['body'])
# print('#'*30)
# print(response.text[0:100])
# print()

# data = {
#     "title": "Sai",
#     "body": "Learning niquests",
#     "userId": 1
# }
# headers = {
#     "Authorization": "Bearer mytoken123"
# }
# params = {
#     "page": 2,
#     "limit": 10,
#     'debug': True
# }
# response = niquests.post(
#     "https://jsonplaceholder.typicode.com/posts",
#     json=data,
#     headers=headers,
#     params=params,
#     timeout=5
# )

# print(response.status_code)
# print(response.json())

#session logiing
# session = niquests.Session()
# session.headers.update({
#     "Authorization": "Bearer mytoken123"
# })

#files
# files = {
#     "file": open("test.pdf", "rb")
# }

# response = niquests.post(
#     "https://api.example.com/upload",
#     files=files
# )



# import asyncio
# import niquests

# async def fetch(url):
#     response = await niquests.aget(url)
#     return response.json()

# async def main():

#     urls = [
#         "https://jsonplaceholder.typicode.com/posts/1",
#         "https://jsonplaceholder.typicode.com/posts/2",
#         "https://jsonplaceholder.typicode.com/posts/3"
#     ]

#     tasks = [fetch(url) for url in urls]

#     results = await asyncio.gather(*tasks)

#     print(results)

# asyncio.run(main())


#-----------------------------------------------------------------------------------------------------------------------------------------------
import asyncio
import niquests
import json
async def main() -> None:
    # r = await niquests.aget('https://api.github.com/events')
    # print(r.status_code)
    # print(r.json())
    # r = await niquests.apost('https://httpbin.org/post', data={'key': 'value'})
    # r = await niquests.aput('https://httpbin.org/put', data={'key': 'value'})
    # r = await niquests.adelete('https://httpbin.org/delete')
    # print(r)

    # payload = {'key1': 'value1', 'key2': 'value2'}
    # r = await niquests.aget('https://httpbin.org/get', params=payload)
    # print(r)
    # print(r.url)
    # print(r.encoding)
    # print(r.text)
    # print(r.json())
    # print(r.headers)
    # print(r.content)

    # url = 'https://api.github.com/some/endpoint'
    # headers = {'user-agent': 'my-app/0.0.1'}
    # r = await niquests.aget(url, headers=headers)
    # print(r)

    # payload = {'key1': 'value1', 'key2': 'value2'}
    # r = niquests.post('https://httpbin.org/post', data=payload)
    # print(r.json()['form'])

    # payload_tuples = [('key1', 'value1'), ('key1', 'value2')]
    # r1 = niquests.post('https://httpbin.org/post', data=payload_tuples)
    # payload_dict = {'key1': ['value1', 'value2']}
    # r2 = niquests.post('https://httpbin.org/post', data=payload_dict)
    # # print(r1.json()['form'])
    # # print(r2.json()['form'])
    # # print(r1.text)
    # # print(r2.text)   ##############test this again
    # print(r1.text)
    # print(r1.text == r2.text)


    url = 'https://api.github.com/some/endpoint'
    payload = {'some': 'data'}
    # r = niquests.post(url, data=json.dumps(payload))
    r = niquests.post(url, json=(payload))
    print(r)

if __name__ == "__main__":
    asyncio.run(main())