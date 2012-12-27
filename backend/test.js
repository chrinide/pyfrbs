var server = require('./server.js'),
    lastID = '';

module.exports = {
  'POST /posts': function(beforeExit, assert) {
    assert.response(server, 
	{
      url: '/posts',
      method: 'POST',
      data: JSON.stringify({ opus: 'opus_test', summary: 'summary_test', tags: ['tag'] }),
      headers: { 'Content-Type': 'application/json' },
	  timeout: 1000
    }, 
	{
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    },
    function(res) {
      var post = JSON.parse(res.body);
      assert.equal('opus_test', post.opus);
      lastID = post._id;
    });
  },

  'GET /posts': function(beforeExit, assert) {
    assert.response(server, 
	{ 
   	  url: '/posts',
	  timeout: 1000
    }, { 
      status: 200, 
      headers: { 'Content-Type': 'application/json' }
    }, 
    function(res) {
      var posts = JSON.parse(res.body);
      assert.type(opuses, 'object');
      posts.forEach(function(p) {
        server.Post.findById(p._id, function(post) {
          post.remove();
        })
      });
    });
  },
};
