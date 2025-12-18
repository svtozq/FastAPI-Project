/* Compatibility shim for jQuery and underscore.js.
 *
 * Copyright Sphinx contributors
 * Released under the two clause BSD licence
 */

/**
 * Small helper function to urldecode strings
 */
jQuery.urldecode = function (x) {
    if (!x) {
        return x;
    }
    return decodeURIComponent(x.replace(/\+/g, ' '));
};

/**
 * Small helper function to urlencode strings
 */
jQuery.urlencode = encodeURIComponent;

/**
 * This function returns the parsed url parameters of the
 * current request.
 */
jQuery.getQueryParameters = function (s) {
    if (typeof s === 'undefined') {
        s = document.location.search;
    }

    const parts = s.substr(s.indexOf('?') + 1).split('&');
    const result = {};

    for (let i = 0; i < parts.length; i++) {
        const tmp = parts[i].split('=', 2);
        const key = jQuery.urldecode(tmp[0]);
        const value = jQuery.urldecode(tmp[1]);

        if (key in result) {
            result[key].push(value);
        } else {
            result[key] = [value];
        }
    }
    return result;
};

/**
 * Highlight a given string on a jquery object
 */
jQuery.fn.highlightText = function (text, className) {

    function highlight(node, addItems) {
        if (node.nodeType === 3) {
            const val = node.nodeValue;
            const pos = val.toLowerCase().indexOf(text);

            if (
                pos >= 0 &&
                !jQuery(node.parentNode).hasClass(className) &&
                !jQuery(node.parentNode).hasClass("nohighlight")
            ) {
                let span;
                const isInSVG = jQuery(node)
                    .closest("body, svg, foreignObject")
                    .is("svg");

                if (isInSVG) {
                    span = document.createElementNS(
                        "http://www.w3.org/2000/svg",
                        "tspan"
                    );
                } else {
                    span = document.createElement("span");
                    span.className = className;
                }

                span.appendChild(
                    document.createTextNode(val.substr(pos, text.length))
                );

                node.parentNode.insertBefore(
                    span,
                    node.parentNode.insertBefore(
                        document.createTextNode(
                            val.substr(pos + text.length)
                        ),
                        node.nextSibling
                    )
                );

                node.nodeValue = val.substr(0, pos);

                if (isInSVG) {
                    const rect = document.createElementNS(
                        "http://www.w3.org/2000/svg",
                        "rect"
                    );
                    const bbox = node.parentElement.getBBox();

                    rect.x.baseVal.value = bbox.x;
                    rect.y.baseVal.value = bbox.y;
                    rect.width.baseVal.value = bbox.width;
                    rect.height.baseVal.value = bbox.height;
                    rect.setAttribute("class", className);

                    addItems.push({
                        parent: node.parentNode,
                        target: rect
                    });
                }
            }
        } else if (!jQuery(node).is("button, select, textarea")) {
            jQuery.each(node.childNodes, function () {
                highlight(this, addItems);
            });
        }
    }

    const addItems = [];

    const result = this.each(function () {
        highlight(this, addItems);
    });

    for (let i = 0; i < addItems.length; i++) {
        jQuery(addItems[i].parent).before(addItems[i].target);
    }

    return result;
};

/**
 * Backward compatibility for jQuery.browser
 */
if (!jQuery.browser) {
    jQuery.uaMatch = function (ua) {
        const uaLower = ua.toLowerCase();

        const match =
            /(chrome)[ \/]([\w.]+)/.exec(uaLower) ||
            /(webkit)[ \/]([\w.]+)/.exec(uaLower) ||
            /(opera)(?:.*version|)[ \/]([\w.]+)/.exec(uaLower) ||
            /(msie) ([\w.]+)/.exec(uaLower) ||
            (uaLower.indexOf("compatible") < 0 &&
                /(mozilla)(?:.*? rv:([\w.]+)|)/.exec(uaLower)) ||
            [];

        return {
            browser: match[1] || "",
            version: match[2] || "0"
        };
    };

    jQuery.browser = {};
    jQuery.browser[
        jQuery.uaMatch(navigator.userAgent).browser
    ] = true;
}
