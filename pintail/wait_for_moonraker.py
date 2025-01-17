import ppb

from .ui import UIScene


class DisconnectedScene(UIScene):
	next: type[ppb.Scene]

	def on_render(self, event, signal):
		event.screen.draw_jpeg(0)
		event.screen.draw_text((0, 0), event.screen.Font.TEN_X_TWENTY, "Connecting...")

	# FIXME: Implement proper connection status handling.
	def on_idle(self, event, signal):
		if hasattr(event, "moonraker"):
			signal(ppb.events.ReplaceScene(self.next))