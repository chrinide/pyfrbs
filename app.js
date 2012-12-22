
/**
 * Module dependencies.
 */

var express = require('express'),
  app = express(),
  mongoose = require('mongoose'),
  models = require('./models'),
  http = require('http'),
  path = require('path'),
  Opus, db;

app.configure(function(){
  app.set('port', process.env.PORT || 3000);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.favicon());
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.static(path.join(__dirname, 'public')));
  app.use(express.logger());
  app.use(express.errorHandler({ 
    dumpExceptions: true, 
    showStack: true 
  }));
});

models.defineModels(mongoose, function() {
  app.Opus = Opus = mongoose.model('Opus');
  db = mongoose.connect('mongodb://localhost/43');
});

app.get('/', function(req, res) {
	res.redirect('/opuses');
});

app.get('/opuses', function(req, res) {
  mongoose.model('Opus').find(function(opuses) {
	  opuses = opuses.map(function(o) {
        return o.__opus;
      });
      res.render('opuses/index.jade', {
		  locals: { opuses: opuses }
	  });
  });
});

app.post('/opuses.:format?', function(req, res) {
  var opus = new Opus(req.body['opus']);
  opus.save(function() {
    switch (req.params.format) {
      case 'json':
        req.send(o.__opus);
        break;
      default:
        res.redirect('/opuses');
    }
  });
});

app.get('/opuses/:id.:format?', function(req, res) {});

app.put('/opuses/:id.:format?', function(req, res) {});

app.del('/opuses/:id.:format?', function(req, res) {});

http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});
