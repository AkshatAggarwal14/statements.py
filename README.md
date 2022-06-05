## statements.py
This is an API that fetches and returns the statement of a CF problem. 

The API can be accessed as `https://statements.deta.dev/statement?c_id={constest_id}&p_id={problem_id}`.

Example: [https://statements.deta.dev/statement?c_id=1539&p_id=C](https://statements.deta.dev/statement?c_id=1539&p_id=C)

Read the docs [here](https://statements.deta.dev/docs).

Recently codeforces started redirecting GET requests without cookies, thus here RCPC Token Decoder is used to get RCPC Token with an initial request and then sending it later in a cookie.