var app = app || {};

(function() {
	'use strict';

	app.Opus = Backbone.Model.extend({

		/* id: unique
		 * title: string
		 * year: string
		 * author: Author.id
		 * original: Opus.id
		 * translator: Translator.id
		 */

		defaults: {
			title: 'Untitled',
			year: 'unknown'
		}

	});

}());
