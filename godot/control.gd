extends Control

@onready var color_picker: ColorPicker = $ColorPicker
@onready var color_label: Label = $Label
@onready var color_rect: ColorRect = $ColorRect

func _ready():
	color_picker.edit_alpha = true
	color_picker.connect("color_changed", _on_color_changed)

func _on_color_changed(color: Color) -> void:
	var is_include_alpha=true
	color_label.text = "選択色: " + color.to_html(is_include_alpha)
	color_rect.color = color
