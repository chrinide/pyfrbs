var express = require('express'),
	mongoose = require('mongoose'),
	http = require('http'),
	path = require('path'),
	crypto = require('crypto');

function hash(pwd, salt, fn) {
	if (3 == arguments.length) {
		crypto.pbkdf2(pwd, salt, 12000, 128, fn);
	} else {
		fn = salt;
		crypto.randomBytes(len, function(err, salt) {
			if (err)
				return fn(err);
			salt = salt.toString('base64');
			crypto.pbkdf2(pwd, salt, 12000, 128, function(err, hash) {
				if (err)
					return fn(err);
				fn(null, salt, hash);
      		});
    	});
  	}
};

var app = express();

app.configure(function(){
	app.use(express.bodyParser());
	app.use(express.cookieParser());
	app.use(express.session({secret: '70p53cr37'}));
	app.use(express.methodOverride());
	app.use(app.router);
	app.use(express.logger());
	app.use(express.errorHandler({ 
		dumpExceptions: true, 
		showStack: true 
  	}));
});

var UserSchema = new mongoose.Schema({
	'name': String,
	'salt': String,
	'hash': String
});

var User = mongoose.model('User', UserSchema);

function auth(req, res, next) {
	if (req.session.user) {
		next();
	} else {
		res.send(403);
	}
}

app.post('/login', function(req, res) {
	User.findOne({name: req.body.username}, function(err, user) {
	    if (!user) {
			user = new User({name: req.body.username, salt: '123!@#abc'});
	    	hash(req.body.password, user.salt, function(err, result) {
				if (!err) {
					user.hash = result;
					user.save(function(err) {
						if (!err) {
							req.session.regenerate(function() {
								req.session.user = user;
								res.redirect('back');
							});
						} else {
							console.log(err);
						};
					});
				} else {
					console.log(err);
				};
			});
		} else {
	    	hash(req.body.password, user.salt, function(err, result) {
				if (!err) {
					if (result == user.hash) {
						req.session.regenerate(function() {
							req.session.user = user;
							res.redirect('back');
						});
					};
				} else {
					console.log(err);
				};
			});
  		};
	});
});

app.get('/logout', function(req, res) {
	req.session.destroy(function() {
		res.redirect('/');
	});
});

var PostSchema = new mongoose.Schema({
	'opus': String,
	'user': mongoose.Schema.ObjectId,
	'date': Date,
	'summary': String,
	'tags': [String]
});

Post = mongoose.model('Post', PostSchema),

app.get('/posts', function(req, res) {
	Post.find({}, function(err, result) {
		if (!err) {
			res.send(result);
		} else {
			console.log(err);
		}
	});
});

app.post('/posts', function(req, res) {
	var post = new Post({
		opus: req.body.opus, 
		date: Date.now(), 
		summary: req.body.summary, 
		tags: req.body.tags
	});
	post.save(function(err) {
		if (!err) {
			res.send(post);
		} else {
			console.log(err);
		}
	});
});

app.get('/posts/:id', function(req, res) {
	Post.findById(req.params.id, 
		function(err, result) {
			if (!err) {
				res.send(result);
			} else {
				console.log(err);
			}
		}
	);
});

app.put('/posts/:id', function(req, res) {
	Post.findByIdAndUpdate(req.params.id, { $set: { opus: req.body.opus, date: Date.now(), summary: req.body.summary, tags: req.body.tags } }, 
		function(err, result) {
			if (!err) {
				res.send(result);
			} else {
				console.log(err);
			}
		}
	);
});

app.delete('/posts/:id', function(req, res) {
	Post.findByIdAndRemove(req.params.id, 
		function(err, result) {
			if (!err) {
				res.send({});
			} else {
				console.log(err);
			}
		}
	);
});

var OpusSchema = new mongoose.Schema({
	'title': String,
	'year': Number,
	'author': mongoose.Schema.ObjectId,
	'original': mongoose.Schema.ObjectId,
	'translator': mongoose.Schema.ObjectId
});

Opus = mongoose.model('Opus', OpusSchema),

app.get('/opuses', function(req, res) {
	Opus.find({}, function(err, result) {
		if (!err) {
			res.send(result);
		} else {
			console.log(err);
		}
	});
});

var AuthorSchema = new mongoose.Schema({
	'name': String,
	'original': mongoose.Schema.ObjectId
});

Author = mongoose.model('Author', AuthorSchema),

app.get('/authors', function(req, res) {
	Author.find({}, function(err, result) {
		if (!err) {
			res.send(result);
		} else {
			console.log(err);
		}
	});
});

var TranslatorSchema = new mongoose.Schema({
	'name': String
});

Translator = mongoose.model('Translator', TranslatorSchema);

mongoose.connect('localhost', '43');

app.listen(3000, function(){
	console.log("Express server listening on port 3000");
});

module.exports = app;
