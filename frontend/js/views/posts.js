var app = app || {};

$(function() {
	'use strict';

	app.PostView = Backbone.View.extend({

		tagName:  'li',

		template: _.template( $('#post-template').html() ),

		events: {
		},

		initialize: function() {
			this.model.on( 'change', this.render, this );
		},

		render: function() {
			this.$el.html( this.template( this.model.toJSON() ) );
			return this;
		}

	});
});
