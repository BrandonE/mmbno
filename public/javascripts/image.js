var Image,
    resourceCache = {},
    readyCallbacks = [];

Image.get = function get(url) {
    return resourceCache[url];
}

// Load an image url or an array of image urls.
Image.load = function load(urlOrArr) {
    if (Array.isArray(urlOrArr)) {
        urlOrArr.forEach(function(url) {
            _load(url);
        });
    } else {
        _load(urlOrArr);
    }
};

Image.onReady = function onReady(func) {
    readyCallbacks.push(func);
}

function _load(url) {
    if(resourceCache[url]) {
        return resourceCache[url];
    }
    else {
        var img = new Image();

        img.onload = function() {
            resourceCache[url] = img;

            if (_isReady()) {
                readyCallbacks.forEach(function(func) { func(); });
            }
        };

        resourceCache[url] = false;
        img.src = url;
    }
}

function _isReady() {
    var ready = true,
        k;

    for (k in resourceCache) {
        if (resourceCache.hasOwnProperty(k) && !resourceCache[k]) {
            ready = false;
        }
    }

    return ready;
}
