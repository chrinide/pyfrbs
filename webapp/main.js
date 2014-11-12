var express = require('express'),
	pg = require('pg').native,
	http = require('http')
 
var app = express();
 
var url = "tcp://user1:pass@127.0.0.1:5432/fuzzy";
var str = "SELECT * FROM variable";

app.get('/', function(req, res) {
	pg.connect(url, function(err, client, done) {
		client.query(str, function(err, result) {
			if (err) {
				res.status(500).send('error');
			} else {
				res.status(200).send('ok');
			}
		});
		done();
	});
});
 
http.createServer(app).listen(2345, function() {
	console.log('listening on port 2345');
});
