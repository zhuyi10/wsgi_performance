WSGI Server Performance Tests<br />
<br />
Testing Environment <br />
---------------------------------------------------------- <br />
2 vagrant ubuntu/trusty64 servers <br />
55.55.55.5: wsgi server host <br />
55.55.55.6: testing host <br />
<br />
Testing Command <br />
---------------------------------------------------------- <br />
ab -n 500 -c 50 "http://55.55.55.5:8081/" <br />
<br />
Results <br />
---------------------------------------------------------- <br />
![alt tag](results.png)