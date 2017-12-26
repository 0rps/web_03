def app(env, start_response):
    raw_query = env.get('QUERY_STRING') or ''
    # raw_query = env.get('HTTP_REFERER')
    # print(raw_query + "asdfsadf")
    # raw_query = "/?a=1&b=2&c=3"
    # pos = raw_query.find('?')
    # if pos != -1:
    #     raw_query = raw_query[pos+1:]
    ans = "\n".join(raw_query.split('&')) or ''
    ans = ans.encode()
    status = '200 OK'
    headers = [('Content-Type',  'text/plain'), ('Content-Length', str(len(ans)))]
    start_response(status, headers)

    return [ans]
