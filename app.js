
/**
 * Module dependencies.
 */

var express = require('express'),
  app = express(),
  mongoose = require('mongoose'),
  models = require('./models'),
  routes = require('./routes'),
  opus = require('./routes/opus'),
  user = require('./routes/user'),
  http = require('http'),
  path = require('path'),
  db, Opus;

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

app.get('/', routes.index);
app.get('/opuses.:format', opus.list);
app.post('/opuses.:format?', opus.add);
app.get('/opuses/:id.:format?', opus.get);
app.put('/opuses/:id.:format?', opus.edit);
app.del('/opuses/:id.:format?', opus.del);
app.get('/users', user.list);

http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});
