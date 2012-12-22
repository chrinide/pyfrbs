exports.list = function(req, res) {
  Opus.find().all(function(opuses) {
    switch (req.params.format) {
      case 'json':
        res.send(opuses.map(function(o) {
          return o.__opus;
        }));
        break;
      default:
        res.render('opuses/index.jade');
    }
  });
};

exports.add = function(req, res) {
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
};

exports.get = function(req, res) {
};

exports.edit = function(req, res) {
};

exports.del = function(req, res) {
};
