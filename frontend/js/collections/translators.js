var app = app || {};

(function() {
	'use strict';

	var TranslatorList = Backbone.Collection.extend({
		model: app.Translator,
	});

	app.Translators = new TranslatorList();

}());
