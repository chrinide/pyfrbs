process.env.NODE_ENV = 'test';

var app = require('../app'),
    lastID = '';

module.exports = {
  'POST /opuses.json': function(assert) {
    assert.response(app, {
      url: '/opuses.json',
      method: 'POST',
      data: JSON.stringify({ document: { title: 'Test' } }),
      headers: { 'Content-Type': 'application/json' }
    }, {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    },

    function(res) {
      var opus = JSON.parse(res.body);
      assert.equal('Test', opus.title);
      lastID = opus._id;
    });
  },

  'HTML POST /opuses': function(assert) {
    assert.response(app, {
      url: '/opuses',
      method: 'POST',
      data: 'opus[title_t]=test',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }, {
      status: 302,
      headers: { 'Content-Type': 'text/plain' }
    });
  },

  'GET /opuses.json': function(assert) {
    assert.response(app, { 
   	  url: '/opuses.json' 
    }, { 
      status: 200, 
      headers: { 'Content-Type': 'application/json' }
    }, 

    function(res) {
      var opuses = JSON.parse(res.body);
      assert.type(opuses, 'object')
      opuses.forEach(function(o) {
        app.Opus.findById(o._id, function(opus) {
          opus.remove();
        })
      });
    });
  },

  'GET /': function(assert) {
    assert.response(app, { 
      url: '/' 
    }, { 
      status: 200, 
	  headers: { 'Content-Type': 'text/html; charset=utf-8' }
	},
      
	function(res) {
      assert.includes(res.body, '<title>Express</title>');
      process.exit();
    });
  }
};
