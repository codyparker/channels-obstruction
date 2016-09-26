from channels.routing import route, route_class
from channels.staticfiles import StaticFilesConsumer
from game import consumers


channel_routing = [
    route_class(consumers.LobbyConsumer,  path=r"^/lobby/"),
    route_class(consumers.GameConsumer,  path=r"^/game/(?P<game_id>\d+)/$")
]
#
# channel_routing = {
#     # # This makes Django serve static files from settings.STATIC_URL, similar
#     # # to django.views.static.serve. This isn't ideal (not exactly production
#     # # quality) but it works for a minimal example.
#     'http.request': StaticFilesConsumer(),
#
#     # Wire up websocket channels to our consumers:
#     'websocket.connect': consumers.ws_connect,
#     'websocket.receive': consumers.ws_receive,
#     # 'websocket.disconnect': consumers.ws_disconnect,
