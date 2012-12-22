exports.defineModels = function defineModels(mongoose) {
  Opus = new mongoose.Schema({
	'author_o': String,
	'author_t': String,
	'translator': String, 
	'title_o': String, 
	'title_t': String, 
	'date_o': String, 
	'date_t': String,
	'source': String,
	'comment': String,
	'tags': [String]
  });
  mongoose.model('Opus', Opus);
};
