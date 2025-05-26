window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng) {
            return L.circleMarker(latlng, {
                radius: 6,
                fillColor: "#3388ff",
                color: "#ffffff",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.9,
            });
        }

    }
});