// based on code from http://stackoverflow.com/questions/8211744/convert-time-interval-given-in-seconds-into-more-human-readable-form
function human_time(milliseconds) {
    var temp = Math.floor(milliseconds / 1000);
    var minutes = Math.floor((temp %= 3600) / 60);
    if (minutes) {
        return minutes + 'min.'
    }
    var seconds = temp % 60;
    if (seconds) {
        return seconds + 'sec.'
    }
    return milliseconds + 'ms'
}

// https://github.com/henrya/js-jquery/tree/master/BinaryTransport
function binarytransport() {
     /**
     *
     * jquery.binarytransport.js
     *
     * @description. jQuery ajax transport for making binary data type requests.
     * @version 1.0
     * @author Henry Algus <henryalgus@gmail.com>
     *
     */

    // use this transport for "binary" data type
    $.ajaxTransport("+binary", function(options, originalOptions, jqXHR){
        // check for conditions and support for blob / arraybuffer response type
        if (window.FormData && ((options.dataType && (options.dataType == 'binary')) || (options.data && ((window.ArrayBuffer && options.data instanceof ArrayBuffer) || (window.Blob && options.data instanceof Blob)))))
        {
            return {
                // create new XMLHttpRequest
                send: function(headers, callback){
            // setup all variables
                    var xhr = new XMLHttpRequest(),
            url = options.url,
            type = options.type,
            async = options.async || true,

            // blob or arraybuffer.
            dataType = options.responseType || "blob",

            data = options.data || null,
            username = options.username || null,
            password = options.password || null;

                    xhr.addEventListener('load', function(){
                var data = {};
                data[options.dataType] = xhr.response;
                // make callback and send data
                callback(xhr.status, xhr.statusText, data, xhr.getAllResponseHeaders());
                    });

                    xhr.open(type, url, async, username, password);

            // setup custom headers
            for (var i in headers ) {
                xhr.setRequestHeader(i, headers[i] );
            }

                    xhr.responseType = dataType;
                    xhr.send(data);
                },
                abort: function(){}
            };
        }
    });
}