var app = app || {};

(function() {
	'use strict';

	app.Author = Backbone.Model.extend({

		/* id: unique
		 * name: string
		 * original: Author.id
		 */

		defaults: {
			name: ''
		}

	});

}());
