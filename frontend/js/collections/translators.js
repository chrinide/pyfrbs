var app = app || {};

(function() {
	'use strict';

	var TranslatorList = Backbone.Collection.extend({

		model: app.Translator,

		localStorage: new Store('translators')

	});

	app.Translators = new TranslatorList();

}());
