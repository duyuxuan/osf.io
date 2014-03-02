this.NodeControl = (function(ko, $, global) {

    /**
     * The ProjectViewModel, scoped to the project header.
     * @param {Object} params The parsed project data returned from the project's API url.
     */
    var ProjectViewModel = function(params) {
        var self = this;
        self._id = params.node.id;
        self.apiUrl = params.node.api_url;
        self.dateCreated = new FormattableDate(params.node.date_created);
        self.dateModified = new FormattableDate(params.node.date_modified);
        self.dateForked = new FormattableDate(params.node.forked_date);
        self.watchedCount = ko.observable(params.node.watched_count);
        self.userIsWatching = ko.observable(params.user.is_watching);
        self.userCanEdit = params.user.can_edit;
        self.description = params.node.description;
        self.title = params.node.title;
        // The button text to display (e.g. "Watch" if not watching)
        self.watchButtonDisplay = ko.computed(function() {
            var text = self.userIsWatching() ? "Unwatch" : "Watch"
            var full = text + " " +self.watchedCount().toString();
            return full;
        });

        // Editable Title and Description
        if (self.userCanEdit) {
            $('#nodeTitleEditable').editable({
                type:  'text',
                pk:    self._id,
                name:  'title',
                url:   self.apiUrl + 'edit/',
                ajaxOptions: {
                    'type': 'POST',
                    "dataType": "json",
                    "contentType": "application/json"
                },
                params: function(params){
                    // Send JSON data
                    return JSON.stringify(params);
                },
                title: 'Edit Title',
                placement: 'bottom',
                success: function(data){
                    document.location.reload(true);
                }
            });
            // TODO(sloria): Repetition here. Rethink.
            $('#nodeDescriptionEditable').editable({
                type:  'text',
                pk:    self._id,
                name:  'description',
                url:   self.apiUrl + 'edit/',
                ajaxOptions: {
                    'type': 'POST',
                    "dataType": "json",
                    "contentType": "application/json"
                },
                params: function(params){
                    // Send JSON data
                    return JSON.stringify(params);
                },
                title: 'Edit Description',
                placement: 'bottom',
                success: function(data){
                    document.location.reload(true);
                },
                emptytext: "No description",
                emptyclass: "text-muted"
            });
        }

        /**
         * Toggle the watch status for this project.
         */
        self.toggleWatch = function() {
            // Send POST request to node's watch API url and update the watch count
            $.ajax({
                url: self.apiUrl + "togglewatch/",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({}),
                contentType: "application/json",
                success: function(data, status, xhr) {
                    // Update watch count in DOM
                    self.userIsWatching(data['watched']);
                    self.watchedCount(data['watchCount']);
                }
            });
        };
    };

    ////////////////
    // Public API //
    ////////////////


    function NodeControl (selector, data, options) {
        var self = this;
        self.selector = selector;
        self.$element = $(self.selector);
        self.data = data;
        self.init();
    }

    NodeControl.prototype.init = function() {
        var self = this;
        ko.applyBindings(new ProjectViewModel(self.data), self.$element[0]);
    };

    return NodeControl;

})(ko, jQuery, window);
