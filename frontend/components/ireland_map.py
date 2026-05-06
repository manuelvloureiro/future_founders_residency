import secrets

from fasthtml.common import Div, NotStr

DUBLIN_LAT, DUBLIN_LON = 53.3498, -6.2603
CORK_LAT, CORK_LON = 51.8985, -8.4756

DUBLIN_STORES = [
    {"name": "Phibsboro", "lat": 53.3580, "lon": -6.2710, "stock": 240, "tone": "warn"},
    {"name": "Rathmines", "lat": 53.3220, "lon": -6.2640, "stock": 220, "tone": "warn"},
    {"name": "Ballybrack", "lat": 53.2410, "lon": -6.1190, "stock": 180, "tone": "warn"},
    {"name": "Clarehall", "lat": 53.4060, "lon": -6.2010, "stock": 260, "tone": "warn"},
    {"name": "Liffey Valley", "lat": 53.3470, "lon": -6.4070, "stock": 320, "tone": "warn"},
    {"name": "Dundrum", "lat": 53.2870, "lon": -6.2440, "stock": 290, "tone": "warn"},
    {"name": "Swords", "lat": 53.4595, "lon": -6.2180, "stock": 290, "tone": "warn"},
]

CORK_STORES = [
    {"name": "Mahon Point", "lat": 51.8910, "lon": -8.4030, "stock": 310, "tone": "risk"},
    {"name": "Wilton", "lat": 51.8830, "lon": -8.5250, "stock": 280, "tone": "risk"},
    {"name": "Douglas", "lat": 51.8760, "lon": -8.4490, "stock": 260, "tone": "risk"},
    {"name": "Bishopstown", "lat": 51.8800, "lon": -8.5320, "stock": 290, "tone": "risk"},
    {"name": "Ballincollig", "lat": 51.8870, "lon": -8.5870, "stock": 240, "tone": "risk"},
    {"name": "Carrigaline", "lat": 51.8160, "lon": -8.3950, "stock": 200, "tone": "risk"},
]

OTHER_STORES = [
    {"name": "Limerick", "lat": 52.6638, "lon": -8.6267, "stock": 210, "tone": "neutral"},
    {"name": "Galway", "lat": 53.2707, "lon": -9.0568, "stock": 230, "tone": "neutral"},
    {"name": "Waterford", "lat": 52.2593, "lon": -7.1101, "stock": 180, "tone": "neutral"},
    {"name": "Kilkenny", "lat": 52.6541, "lon": -7.2448, "stock": 160, "tone": "neutral"},
    {"name": "Sligo", "lat": 54.2697, "lon": -8.4694, "stock": 140, "tone": "neutral"},
    {"name": "Drogheda", "lat": 53.7189, "lon": -6.3478, "stock": 170, "tone": "neutral"},
    {"name": "Athlone", "lat": 53.4239, "lon": -7.9407, "stock": 150, "tone": "neutral"},
    {"name": "Tralee", "lat": 52.2706, "lon": -9.7000, "stock": 130, "tone": "neutral"},
]


def ireland_map(cities: dict) -> Div:
    dublin = cities["dublin"]
    cork = cities["cork"]

    def fmt_delta(city: dict) -> tuple[str, str, str]:
        delta = city["price_delta_pct"]
        if delta >= 0:
            arrow = "▲"
            tone = "up"
            sign = "+"
        else:
            arrow = "▼"
            tone = "down"
            sign = "−"
        body = (
            f"€{city['current_price_eur']:.2f} → €{city['recommended_price_eur']:.2f} "
            f"({sign}{abs(delta):.1f}%)"
        )
        return arrow, tone, body

    dub_arrow, dub_tone, dub_price = fmt_delta(dublin)
    cor_arrow, cor_tone, cor_price = fmt_delta(cork)

    map_id = f"keith-map-{secrets.token_hex(4)}"

    all_stores = (
        [{**s, "city": "Dublin"} for s in DUBLIN_STORES]
        + [{**s, "city": "Cork"} for s in CORK_STORES]
        + [{**s, "city": s["name"]} for s in OTHER_STORES]
    )
    stores_js = ",".join(
        f"{{lat:{s['lat']},lon:{s['lon']},name:{s['name']!r},stock:{s['stock']},tone:{s['tone']!r}}}"
        for s in all_stores
    )

    init_script = f"""
(function() {{
  function init() {{
    var el = document.getElementById('{map_id}');
    if (!el || !window.L) {{ return false; }}
    if (el.dataset.keithInit === '1') {{ return true; }}
    el.dataset.keithInit = '1';

    var dublin = [{DUBLIN_LAT}, {DUBLIN_LON}];
    var cork = [{CORK_LAT}, {CORK_LON}];

    var map = L.map(el, {{
      zoomControl: false,
      attributionControl: true,
      scrollWheelZoom: false,
      dragging: false,
      doubleClickZoom: false,
      boxZoom: false,
      keyboard: false,
      touchZoom: false,
    }});

    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19,
    }}).addTo(map);

    var irelandBounds = L.latLngBounds([[51.35, -10.7], [55.45, -5.3]]);
    map.fitBounds(irelandBounds, {{padding: [20, 20]}});

    var stores = [{stores_js}];
    stores.forEach(function(s) {{
      var icon = L.divIcon({{
        className: '',
        html: '<div class="keith-store keith-store-' + s.tone + '" title="' + s.name + ' · ' + s.stock + 'u"></div>',
        iconSize: [10, 10],
        iconAnchor: [5, 5],
      }});
      L.marker([s.lat, s.lon], {{icon: icon, interactive: false}}).addTo(map);
    }});

    var dublinIcon = L.divIcon({{
      className: '',
      html: '<div class="keith-pin-wrap"><span class="keith-pin-halo keith-pin-halo-dublin"></span><span class="keith-pin keith-pin-dublin"></span></div>',
      iconSize: [18, 18],
      iconAnchor: [9, 9],
    }});
    var corkIcon = L.divIcon({{
      className: '',
      html: '<div class="keith-pin-wrap"><span class="keith-pin-halo keith-pin-halo-cork"></span><span class="keith-pin keith-pin-cork"></span></div>',
      iconSize: [18, 18],
      iconAnchor: [9, 9],
    }});

    L.marker(dublin, {{icon: dublinIcon}}).addTo(map);
    L.marker(cork, {{icon: corkIcon}}).addTo(map);

    var dublinLabel = L.divIcon({{
      className: '',
      html: '<div class="keith-label"><span class="keith-label-name">{dublin['name']}</span><span class="keith-label-emoji">{dublin['emoji']}</span><span class="keith-label-price">{dub_price}</span><span class="keith-label-arrow keith-label-arrow-{dub_tone}">{dub_arrow}</span></div>',
      iconSize: [240, 28],
      iconAnchor: [252, 13],
    }});
    var corkLabel = L.divIcon({{
      className: '',
      html: '<div class="keith-label"><span class="keith-label-name">{cork['name']}</span><span class="keith-label-emoji">{cork['emoji']}</span><span class="keith-label-price">{cor_price}</span><span class="keith-label-arrow keith-label-arrow-{cor_tone}">{cor_arrow}</span></div>',
      iconSize: [240, 28],
      iconAnchor: [-12, 13],
    }});
    L.marker(dublin, {{icon: dublinLabel, interactive: false}}).addTo(map);
    L.marker(cork, {{icon: corkLabel, interactive: false}}).addTo(map);

    var routePoints = [cork, dublin];
    var arrow = L.polyline(routePoints, {{
      color: '#0f172a',
      weight: 2.5,
      opacity: 0.85,
      dashArray: '6 5',
      lineCap: 'round',
    }}).addTo(map);

    var lorryIcon = L.divIcon({{
      className: '',
      html: '<div class="keith-lorry">🚚</div>',
      iconSize: [28, 28],
      iconAnchor: [14, 14],
    }});
    var lorryMarker = L.marker(cork, {{icon: lorryIcon, interactive: false, zIndexOffset: 1000}}).addTo(map);

    var arrowLabel = L.divIcon({{
      className: '',
      html: '<div class="keith-arrow-label">+400 units &rarr;</div>',
      iconSize: [110, 20],
      iconAnchor: [55, 10],
    }});
    var midLat = (dublin[0] + cork[0]) / 2;
    var midLon = (dublin[1] + cork[1]) / 2;
    L.marker([midLat, midLon], {{icon: arrowLabel, interactive: false}}).addTo(map);

    var animStart = null;
    var animDurationMs = 4000;
    var animPauseMs = 1500;
    function animateLorry(ts) {{
      if (!animStart) animStart = ts;
      var elapsed = ts - animStart;
      var cycle = animDurationMs + animPauseMs;
      var t = (elapsed % cycle) / animDurationMs;
      if (t > 1) t = 1;
      var lat = cork[0] + (dublin[0] - cork[0]) * t;
      var lon = cork[1] + (dublin[1] - cork[1]) * t;
      lorryMarker.setLatLng([lat, lon]);
      requestAnimationFrame(animateLorry);
    }}
    requestAnimationFrame(animateLorry);

    setTimeout(function() {{ map.invalidateSize(); }}, 60);
    return true;
  }}

  if (init()) return;
  var tries = 0;
  var t = setInterval(function() {{
    tries++;
    if (init() || tries > 40) clearInterval(t);
  }}, 100);
}})();
"""

    return Div(
        Div(id=map_id, cls="keith-map"),
        NotStr(f"<script>{init_script}</script>"),
        cls="w-full",
    )
