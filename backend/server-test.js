var request = require('supertest'), 
	app     = require('./server'),
    assert  = require("assert");
	
describe('GET /posts', function() {
	it('200', function(done) {
		request(app)
		.get('/posts')
		.expect(200)
		.end(function(err, res) {
			done();
		})
    })
});

describe('GET /posts/:id', function() {
	it('404', function(done) {
		request(app)
		.get('/posts/123')
		.expect(404)
		.end(function(err, res) {
			done();
		})
    })
});

describe('POST /posts', function() {
	it('401', function(done) {
		request(app)
		.post('/posts')
		.send({opus: "test", tags: "test", summary: "test"})
		.expect(401)
		.end(function(err, res) {
			done();
		})
    })
});

describe('PUT /posts/:id', function() {
	it('401', function(done) {
		request(app)
		.put('/posts/123')
		.send({opus: "test", tags: "test", summary: "test"})
		.expect(401)
		.end(function(err, res) {
			done();
		})
    })
});

describe('DEL /posts/:id', function() {
	it('401', function(done) {
		request(app)
		.del('/posts/123')
		.expect(401)
		.end(function(err, res) {
			done();
		})
    })
});

describe('POST /login', function() {
	it('200', function(done) {
		request(app)
		.post('/login')
		.send({username: "test", password: "test"})
		.expect(200)
		.end(function(err, res) {
			done();
		})
    })
});

describe('GET /logout', function() {
	it('200', function(done) {
		request(app)
		.get('/logout')
		.expect(200)
		.end(function(err, res) {
			done();
		})
    })
});

describe('GET /opuses', function() {
	it('200', function(done) {
		request(app)
		.get('/opuses')
		.expect(200)
		.end(function(err, res) {
			done();
		})
    })
});

describe('GET /authors', function() {
	it('200', function(done) {
		request(app)
		.get('/authors')
		.expect(200)
		.end(function(err, res) {
			done();
		})
    })
});
