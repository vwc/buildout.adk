/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global Modernizr, jQuery:false, document:false */
'use strict';

(function ($) {
    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {return; }
        // Application specific javascript code goes here
        if (!Modernizr.csstransitions) { // Test if CSS transitions are supported
            $(function () {
                $('.dim-in').on('load', function () {
                    $(this).animate({opacity: '1'}, {queue: false, duration: 500});
                });
            });
        }
    }
    );
}(jQuery));
