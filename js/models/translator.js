var app = app || {};

(function() {
	'use strict';

	app.Translator = Backbone.Model.extend({

		/* id: unique
		 * name: string
		 */

		defaults: {
			name: ''
		}

	});

}());
