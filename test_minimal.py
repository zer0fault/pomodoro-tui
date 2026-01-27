#!/usr/bin/env python
"""
Minimal Textual app to test if ANY input works.
"""
from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Footer, Button
from textual.binding import Binding


class MinimalTestApp(App):
    """Minimal app to test input."""

    CSS = """
    Screen {
        align: center middle;
    }

    #message {
        width: 60;
        height: 10;
        border: heavy green;
        padding: 2;
        text-align: center;
    }

    Button {
        margin: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("space", "test_space", "Test Space"),
    ]

    def __init__(self):
        super().__init__()
        self.key_count = 0
        self.click_count = 0

    def compose(self) -> ComposeResult:
        """Create widgets."""
        yield Header()
        yield Static(
            "MINIMAL INPUT TEST\n\n"
            "Press ANY key\n"
            "Click the button\n"
            "Press Q to quit\n\n"
            "Keys pressed: 0\n"
            "Clicks: 0",
            id="message"
        )
        yield Button("Click Me!", id="test-button", variant="success")
        yield Footer()

    def on_key(self, event) -> None:
        """Called for ANY key press."""
        self.key_count += 1
        self.update_message(f"Key pressed: {event.key}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when button clicked."""
        self.click_count += 1
        self.update_message("Button clicked!")

    def action_test_space(self) -> None:
        """Test space action."""
        self.notify("SPACE ACTION WORKED!", severity="information")

    def action_quit(self) -> None:
        """Quit."""
        self.exit()

    def update_message(self, last_action: str) -> None:
        """Update the message."""
        message = self.query_one("#message", Static)
        message.update(
            f"MINIMAL INPUT TEST\n\n"
            f"Last action: {last_action}\n\n"
            f"Total keys pressed: {self.key_count}\n"
            f"Total clicks: {self.click_count}\n\n"
            f"Press Q to quit"
        )


if __name__ == "__main__":
    print("="*60)
    print("RUNNING MINIMAL INPUT TEST")
    print("="*60)
    print("If you see the app but nothing responds:")
    print("  - Try pressing ANY key")
    print("  - Try clicking the button")
    print("  - Try pressing Q")
    print("="*60)
    print()

    app = MinimalTestApp()
    app.run()

    print()
    print("="*60)
    print(f"Test Results:")
    print(f"  Keys pressed: {app.key_count}")
    print(f"  Button clicks: {app.click_count}")
    print("="*60)
