'use strict';
(function ($) {
    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {
            return;
        }
        if (!Modernizr.csstransitions) {
            $(function () {
                $('.dim-in').on('load', function () {
                    $(this).animate({ opacity: '1' }, {
                        queue: false,
                        duration: 500
                    });
                });
            });
        }
    });
}(jQuery));