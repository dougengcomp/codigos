import httpx

async def main():
    async with httpx.AsyncClient(http1=False, http2=True) as client:
        # Perform the search request
        response = client.get("https://www.ufrgs.br/ifch/index.php")
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Search results:")
            print(response.text)
            print(f"http version is: {response.http_version}")
            # Check if the connection used HTTP/2
            if 'HTTP/2' in response.http_version:
                print("Connection type: HTTP/2")
            else:
                print("Connection type: HTTP/1.1 or other")
        else:
            print(f"Failed to perform search. Status code: {response.status_code}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())