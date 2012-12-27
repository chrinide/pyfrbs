var app = app || {};

$(function() {
	'use strict';

	app.PostView = Backbone.View.extend({

		tagName:  'li',

		template: _.template( $('#post-template').html() ),

		events: {
			'dblclick label':	'edit',
			'keypress .edit':	'updateOnEnter',
			'blur .edit':		'close'
		},

		initialize: function() {
			this.model.on( 'change', this.render, this );
			this.model.on( 'destroy', this.remove, this );
		},

		render: function() {
			this.$el.html( this.template( this.model.toJSON() ) );

			this.input = this.$('.edit');
			return this;
		},

		edit: function() {
			this.$el.addClass('editing');
			this.input.focus();
		},

		close: function() {
			var value = this.input.val().trim();

			if ( value ) {
				this.model.save({ summary: value });
			} else {
				this.clear();
			}

			this.$el.removeClass('editing');
		},

		updateOnEnter: function( e ) {
			if ( e.which === ENTER_KEY ) {
				this.close();
			}
		},

		clear: function() {
			this.model.destroy();
		}
	});
});
