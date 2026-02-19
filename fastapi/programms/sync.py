def blocking_fetch_urls(urls):
    results = []
    start_time = time.time()
    
    for url in urls:
        try:
            print(f"Fetching {url}")
            response = requests.get(url)
            results.append({
                'url': url,
                'status': response.status_code,
                'length': len(response.text)
            })
        except Exception as e:
            results.append({
                'url': url,
                'error': str(e)
            })
    
    return results

