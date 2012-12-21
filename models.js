var mongoose = require('mongoose').Mongoose;

mongoose.model('opus', {
	  properties: [
		'author_o', 
		'author_t', 
		'translator', 
		'title_o', 
		'title_t', 
		'date_o', 
		'date_t',
		'source',
		'comment',
		'tags'
	  ],
	  indexes: [
	    'title'
	  ]
});

exports.opus = function(db) {
	  return db.model('opus');
};
