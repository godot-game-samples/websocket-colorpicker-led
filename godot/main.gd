extends Node2D

const PORT = 9080

var tcp_server := TCPServer.new()
var peers: Dictionary = {}

@onready var color_picker: ColorPicker = %ColorPicker

func _ready() -> void:
	if tcp_server.listen(PORT) != OK:
		print("Unable to start server.")
		set_process(false)
	
	color_picker.connect("color_changed", _on_color_changed)
	print("🎨 ColorPicker ready.")

func _process(_delta: float) -> void:
	while tcp_server.is_connection_available():
		var conn: StreamPeerTCP = tcp_server.take_connection()
		if conn:
			var peer: WebSocketPeer = WebSocketPeer.new()
			if peer.accept_stream(conn) == OK:
				var id := conn.get_connected_host() + ":" + str(conn.get_connected_port())
				peers[id] = peer
				print("🔌 client connection: %s" % id)
			else:
				print("⚠️ Connection Failure")

	for id in peers.keys():
		var peer: WebSocketPeer = peers[id]
		peer.poll()

		while peer.get_available_packet_count() > 0:
			var packet := peer.get_packet()
			var msg := packet.get_string_from_utf8()
			print("📨 reception: ", msg)

func _exit_tree() -> void:
	for id in peers:
		peers[id].close()
	tcp_server.stop()

func _on_color_changed(new_color: Color) -> void:
	var is_include_alpha=true
	var color_hex := new_color.to_html(is_include_alpha)
	print("🎨 Color changed to: ", color_hex)

	var json := {"type": "color", "value": color_hex}
	var packet := JSON.stringify(json).to_utf8_buffer()

	for peer in peers.values():
		if peer.get_ready_state() == WebSocketPeer.STATE_OPEN:
			peer.put_packet(packet)
